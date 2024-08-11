# Create your views here.
import random
import stripe
from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from carro.carro import Carro
from products.models import Product
from usuario.decorator import role_required
from .models import Purchase, SolicitudStripeItem

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


STRIPE_SECRET_KEY = "sk_test_51PbVREDUVZyD9P5hMx44bCmUwBMlf0xjyLHEGrCliSwPrcyADzuH7RtHmfmtDWacsjoYuUcHgauWBrFTHFZHx6lP00yxOBc8hs"
stripe.api_key = STRIPE_SECRET_KEY



# BASE_ENDPOINT= config("BASE_ENDPOINT", default="http://127.0.0.1:8000")
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




#
# @csrf_exempt
# def create_checkout_session(request):
#     if request.method == 'POST':
#         # Create a new Stripe checkout session
#         session = stripe.checkout.Session.create(
#             line_items=[{
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {
#                         'name': 'T-shirt',
#                     },
#                     'unit_amount': 2000,
#                 },
#                 'quantity': 2,
#             }],
#             mode='payment',
#             success_url=request.build_absolute_uri(reverse('purchases:success')),
#             cancel_url=request.build_absolute_uri(reverse('purchases:stopped')),
#         )
#         # Redirect the user to the Stripe checkout page
#         return redirect(session.url, status_code=303)
#     else:
#         return HttpResponse('Method not allowed', status=405)
#



@login_required
def buy_cart_stripe(request):
    total = 0
    if not request.method == "POST":
        return HttpResponseBadRequest()
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("Debe autenticarse")

    purchase = Purchase.objects.create(user=request.user)
    request.session['purchase_id'] = purchase.id

    session = request.session
    carro = session.get('carro', {})

    if not carro:
        return HttpResponseBadRequest("El carrito está vacío.")

    cart_items = carro.items()




    line_items = []
    for item_id, item in cart_items:
        product = get_object_or_404(Product, pk=item["product_id"])
        line_items.append({
            "price": product.stripe_price_id,
            "quantity": item["cantidad"],
        })


    for item_id, item in cart_items:
        product = get_object_or_404(Product, pk=item["product_id"])
        purchase.product.add(product)
        purchase.guardar_producto(product=product, quantity=item["cantidad"], purchase=purchase)
        total = total + item["subtotal"]

    purchase.stripe_price = total
    purchase.save()




    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=f"{BASE_ENDPOINT}{reverse('pedidos_stripe:success_cart')}",
        cancel_url=f"{BASE_ENDPOINT}{reverse('pedidos_stripe:stopped')}",
    )
    purchase.stripe_checkout_session_id = checkout_session.id
    purchase.save()


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

    completado = request.GET.get('completado' or None)

    if completado:
        if completado == 'true':
            completado = True
        else:
            completado = False
        solicitudes = solicitudes.filter(completed=completado)




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



def purchase_detail(request, purchase_id):
    purchase = get_object_or_404(Purchase, pk=purchase_id)
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
