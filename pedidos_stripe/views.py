# Create your views here.
import random
import stripe
from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from carro.carro import Carro
from extra.models import Destinatario
from products.models import Product
from usuario.decorator import role_required
from .models import Purchase, SolicitudStripeItem

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.urls import reverse
from stripe.error import APIConnectionError
import stripe


STRIPE_SECRET_KEY = "sk_test_51PbVREDUVZyD9P5hMx44bCmUwBMlf0xjyLHEGrCliSwPrcyADzuH7RtHmfmtDWacsjoYuUcHgauWBrFTHFZHx6lP00yxOBc8hs"
stripe.api_key = STRIPE_SECRET_KEY



BASE_ENDPOINT= "http://127.0.0.1:8000"


cantidad = 0
def purchase_start_view(request):
    if not request.method == "POST":
        return HttpResponseBadRequest()
    if not request.user.is_authenticated:
        return HttpResponseBadRequest()
    handle = request.POST.get("handle")
    obj = Product.objects.get(handle=handle)
    stripe_price_id = obj.stripe_price_id
    if stripe_price_id is None:
        return HttpResponseBadRequest()

    purchase = Purchase.objects.create(user=request.user, product=obj)
    request.session['purchase_id'] = purchase.id
    success_path = reverse("pedidos_stripe:success")
    if not success_path.startswith("/"):
        success_path = f"/{success_path}"
    cancel_path = reverse("pedidos_stripe:stopped")
    success_url = f"{BASE_ENDPOINT}{success_path}"
    cancel_url = f"{BASE_ENDPOINT}{cancel_path}"
    quantity = int(request.POST.get('quantity', 1))
    global cantidad
    cantidad = quantity
    checkout_session = stripe.checkout.Session.create(
        line_items = [
            {
                "price": stripe_price_id,
                "quantity": quantity,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url
    )
    purchase.stripe_checkout_session_id = checkout_session.id
    purchase.save()
    return HttpResponseRedirect(checkout_session.url)





def buy_cart_stripe(request,destinatario_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Debes estar registrado para poder realizar compras.')
        return HttpResponseRedirect(reverse('usuario:login'))



    if request.method == 'POST':
        destinatario = get_object_or_404(Destinatario, pk=destinatario_id)



    total = 0
    if not request.method == "POST":
        return HttpResponseBadRequest()

    purchase = Purchase.objects.create(user=request.user)
    request.session['purchase_id'] = purchase.id
    if destinatario:
        if destinatario.nombre:
            purchase.nombre = destinatario.nombre
        if destinatario.apellidos:
            purchase.apellidos = destinatario.apellidos
        if destinatario.telefono:
            purchase.telefono = destinatario.telefono
        if destinatario.carnet_de_identidad:
            purchase.carnet_de_identidad = destinatario.carnet_de_identidad
        if destinatario.correo_electronico:
            purchase.correo_electronico = destinatario.correo_electronico
        if destinatario.direccion:
            purchase.direccion = destinatario.direccion
        if destinatario.municipio:
            purchase.municipio = destinatario.municipio
        if destinatario.instrucciones_entrega:
            purchase.instrucciones_entrega = destinatario.instrucciones_entrega


    session = request.session
    carro = session.get('carro', {})

    if not carro:
        return HttpResponseBadRequest("El carrito está vacío.")

    cart_items = carro.items()
    stock_error_products = []
    line_items = []
    for item_id, item in cart_items:
        product = get_object_or_404(Product, pk=item["product_id"])
        line_items.append({
            "price": product.stripe_price_id,
            "quantity": item["cantidad"],
        })
        if product.supply < item["cantidad"]:
            stock_error_products.append(product.name)

    if stock_error_products:
        stock_error = "Lo sentimos, no hay suficiente disponibilidad de los siguientes productos: " + ", ".join(
            stock_error_products) + ". Te recomendamos que los retires del carrito para continuar con tu compra."
        context = {
            "stock_error": stock_error
        }
        return render(request, "purchases/cart.html", context)
    else:
        stock_error = None




    for item_id, item in cart_items:
        product = get_object_or_404(Product, pk=item["product_id"])
        purchase.product.add(product)
        purchase.guardar_producto(product=product, quantity=item["cantidad"], purchase=purchase)
        total = total + item["subtotal"]

    purchase.stripe_price = total
    purchase.save()

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=f"{BASE_ENDPOINT}{reverse('pedidos_stripe:success_cart')}",
            cancel_url=f"{BASE_ENDPOINT}{reverse('pedidos_stripe:stopped')}",
        )
        purchase.stripe_checkout_session_id = checkout_session.id
        purchase.save()
    except APIConnectionError:
        # Manejo de error de conexión con Stripe
        stock_error =  'Error de conexión con Stripe. Por favor, intenta más tarde.'
        return render(request, "purchases/cart.html", {"stock_error": stock_error})

    except Exception as e:
        # Manejo de otras excepciones
        stock_error = f'Ocurrió un error inesperado: {str(e)}'
        return render(request, "purchases/cart.html", {"stock_error": stock_error})


    return HttpResponseRedirect(checkout_session.url)

@login_required
def pedidos_stripe(request):
    filter_usuario = request.GET.get('usuario' or None)
    if request.user.usuario.rol.nombre == 'admin':
        # Filtrar las solicitudes en base a los parámetros
        if filter_usuario:
            solicitudes = Purchase.objects.filter(user__username__icontains=filter_usuario)
        else:
            solicitudes = Purchase.objects.all()
    else:
        solicitudes = Purchase.objects.filter(user=request.user)

    entrega = request.GET.get('estado' or None)
    if entrega:
        solicitudes = solicitudes.filter(entrega=entrega)

    solicitudes = solicitudes.order_by('-timestamp')

    completado = request.GET.get('completado' or None)


    if completado:
        if completado == 'false':
            solicitudes = solicitudes.filter(completed=False)
        else:
            solicitudes = solicitudes.filter(completed=True)
    else:
        solicitudes = solicitudes.filter(completed=True)




    # Paginar las solicitudes
    page_size = 20  # Número de solicitudes por página
    paginator = Paginator(solicitudes, page_size)
    page_number = request.GET.get('page', 1)

    try:
        page_solicitudes = paginator.page(page_number)
    except PageNotAnInteger:
        page_solicitudes = paginator.page(1)
    except EmptyPage:
        page_solicitudes = paginator.page(paginator.num_pages)



    context = {
        'pedidos_stripe': page_solicitudes,
        'filter_usuario': filter_usuario,
    }
    return render(request, 'purchases/solicitud_list.html', context)



@login_required
def purchase_detail(request, purchase_id):
    purchase = get_object_or_404(Purchase, pk=purchase_id)
    if purchase.user != request.user and request.user.usuario.rol.nombre != 'admin':
        messages.warning(request, 'No tiene acceso a ese pedido')
        return HttpResponseRedirect(reverse('pedidos_stripe:purchases_stripe'))
    solicitud_items = SolicitudStripeItem.objects.filter(solicitud=purchase)


    context = {
        'purchase': purchase,
        'solicitud_items': solicitud_items,
    }

    return render(request, 'purchases/solicitud/solicitud_stripe_detail.html', context)



def purchase_success_cart_view(request):
    purchase_id = request.session.get("purchase_id")
    session = request.session
    carro = session.get('carro', {})
    cart_items = carro.items()


    for item_id, item in cart_items:
        product = get_object_or_404(Product, pk=item["product_id"])
        product.supply = product.supply - item["cantidad"]
        product.save()


    carro = Carro(request)
    carro.limpiar_carro()

    if purchase_id:
        purchase = Purchase.objects.get(id=int(purchase_id))
        purchase.completed = True
        purchase.save()
        del request.session['purchase_id']

        # Enviar email al usuario si tiene
        if purchase.user.email:
            context = {
                "total": purchase.stripe_price,
                "products": purchase.items.all(),
            }
            html_message = render_to_string('purchases/email/pago_con_exito_stripe.html', context)
            plain_message = strip_tags(html_message)
            subject_email = "Pago efectuado con exito"
            user_email = purchase.user.email

            send_mail(
                subject=subject_email,
                message=plain_message,
                from_email=EMAIL_HOST_USER,
                recipient_list=[user_email],
                html_message=html_message,
                fail_silently=False,
            )
        return HttpResponseRedirect(reverse("pedidos_stripe:purchases_stripe"))
    return HttpResponseRedirect(reverse("products:list"))



def purchase_stopped_view(request):
    purchase_id = request.session.get("purchase_id")
    if purchase_id:
        del request.session['purchase_id']
        return HttpResponseRedirect(reverse("products:list"))
    return HttpResponseRedirect(reverse("products:list"))



def purchase_success_view(request):
    purchase_id = request.session.get("purchase_id")


    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        global cantidad
        product = purchase.product
        product.supply = product.supply - cantidad
        cantidad = 0
        product.save()
        purchase.completed = True
        purchase.save()
        del request.session['purchase_id']
        return HttpResponseRedirect(purchase.product.get_absolute_url())
    return HttpResponse(f"Finished {purchase_id}")


@role_required(['Proveedor'])
def ventas(request):
    ventas = SolicitudStripeItem.objects.filter(product__user=request.user,solicitud__completed=True)
    ventas = ventas.order_by('-solicitud__timestamp')
    # Paginar los productos


    page_size = 20  # Número de solicitudes por página
    paginator = Paginator(ventas, page_size)
    page_number = request.GET.get('page', 1)

    try:
        page_solicitudes = paginator.page(page_number)
    except PageNotAnInteger:
        page_solicitudes = paginator.page(1)
    except EmptyPage:
        page_solicitudes = paginator.page(paginator.num_pages)



    context = {
        "ventas":page_solicitudes,
    }

    return render(request,'purchases/stripe/ventas.html',context)


@role_required(['Proveedor'])
def ver_venta(request,venta_id):
    venta = SolicitudStripeItem.objects.get(id=venta_id)
    if venta.product.user != request.user:
        messages.warning(request, 'No tiene acceso para esa venta')
        return HttpResponseRedirect(reverse('pedidos_stripe:ventas'))

    context = {
        "venta":venta
    }
    return render(request,'purchases/stripe/ver_venta.html',context)


@role_required(['admin'])
def aceptar_pedido(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    if purchase.entrega == 'pending':
        purchase.entrega = 'onway'
        purchase.save()

    return redirect('pedidos_stripe:ver_solicitud_stripe', purchase_id=purchase_id)


@role_required(['admin'])
def cancelar_pedido(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)

    if purchase.entrega == 'pending':
        purchase.entrega = 'canceled'
        purchase.save()

    return redirect('pedidos_stripe:ver_solicitud_stripe', purchase_id=purchase_id)



@role_required(['admin'])
def entregar_pedido(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)

    if purchase.entrega == 'onway':
        purchase.entrega = 'accepted'
        purchase.save()

    return redirect('pedidos_stripe:ver_solicitud_stripe', purchase_id=purchase_id)
