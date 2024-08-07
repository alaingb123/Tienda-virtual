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
from .form import SolicitudZelleForm
from .models import Purchase, SolicitudZelle, SolicitudZelleItem
from django.core.mail import EmailMessage,send_mail
from .env import config  # Si está en el mismo directorio


STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default=None)
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
    success_path = reverse("purchases:success")
    if not success_path.startswith("/"):
        success_path = f"/{success_path}"
    cancel_path = reverse("purchases:stopped")
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


def purchase_success_cart_view(request):
    session = request.session
    carro = session.get('carro', {})
    cart_items = carro.items()

    for item_id, item in cart_items:
        product = get_object_or_404(Product, pk=item["product_id"])
        product.supply = product.supply - item["cantidad"]
        product.save()

    carro = Carro(request)
    carro.limpiar_carro()
    purchase_id = request.session.get("purchase_id")
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        purchase.completed = True
        purchase.save()
        del request.session['purchase_id']
        return HttpResponseRedirect(purchase.product.get_absolute_url())
    return HttpResponse(f"Finished {purchase_id}")


def purchase_stopped_view(request):
    purchase_id = request.session.get("purchase_id")
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        product = purchase.product
        del request.session['purchase_id']
        return HttpResponseRedirect(product.get_absolute_url())
    return HttpResponse("Stopped")


# This example sets up an endpoint using the Flask framework.
# Watch this video to get started: https://youtu.be/7Ul1vfmsDck.



STRIPE_SECRET_KEY = "sk_test_51PbVREDUVZyD9P5hMx44bCmUwBMlf0xjyLHEGrCliSwPrcyADzuH7RtHmfmtDWacsjoYuUcHgauWBrFTHFZHx6lP00yxOBc8hs"
stripe.api_key = STRIPE_SECRET_KEY


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        # Create a new Stripe checkout session
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'T-shirt',
                    },
                    'unit_amount': 2000,
                },
                'quantity': 2,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('purchases:success')),
            cancel_url=request.build_absolute_uri(reverse('purchases:stopped')),
        )
        # Redirect the user to the Stripe checkout page
        return redirect(session.url, status_code=303)
    else:
        return HttpResponse('Method not allowed', status=405)


#
# def purchase_start_view(request):
#     if not request.method == "POST":
#         return HttpResponseBadRequest()
#     if not request.user.is_authenticated:
#         return HttpResponseBadRequest()
#     handle = request.POST.get("handle")
#     obj = Product.objects.get(handle=handle)
#     stripe_price_id = obj.stripe_price_id
#     if stripe_price_id is None:
#         return HttpResponseBadRequest()
#
#     purchase = Purchase.objects.create(user=request.user, product=obj)
#     request.session['purchase_id'] = purchase.id
#
#
#     session = stripe.checkout.Session.create(
#         line_items=[{
#             'price_data': {
#                 'currency': 'usd',
#                 'product_data': {
#                     'name': obj.name,
#                 },
#                 'unit_amount': obj.stripe_price,
#             },
#             'quantity': 1,
#         }],
#         mode='payment',
#         success_url=request.build_absolute_uri(reverse('purchases:success')),
#         cancel_url=request.build_absolute_uri(reverse('purchases:stopped')),
#     )
#     purchase.stripe_checkout_session_id = session.id
#     purchase.save()
#     return HttpResponseRedirect(session.url)
#

def cart(request):
    return render(request,"purchases/cart.html")


def buy_cart(request):
    session = request.session
    carro = session.get('carro', {})
    cart_items = carro.items()

    line_items = []
    for item_id, item in cart_items:
        product = get_object_or_404(Product, pk=item["product_id"])
        line_items.append({
            "price": product.stripe_price_id,
            "quantity": item["cantidad"],
        })


    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=f"{BASE_ENDPOINT}{reverse('purchases:success_cart')}",
        cancel_url=f"{BASE_ENDPOINT}{reverse('purchases:stopped')}",
    )


    return HttpResponseRedirect(checkout_session.url)




from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def create_solicitud_zelle(request):
    total = 0
    session = request.session
    carro = session.get('carro', {})
    cart_items = carro.items()

    if request.method == 'POST':
        form = SolicitudZelleForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            solicitud_zelle = form.save(commit=False)

            solicitud_zelle.amount = total
            solicitud_zelle.save()

            products = []
            for item_id, item in cart_items:
                product = get_object_or_404(Product, pk=item["product_id"])
                solicitud_zelle.products.add(product)
                solicitud_zelle.guardar_producto(product=product, quantity=item["cantidad"], solicitud=solicitud_zelle)
                total = total + item["subtotal"]
                products.append({
                    "name": product.name,
                    "price": product.price,
                    "quantity": item["cantidad"],
                    "image": product.image.url
                })

            solicitud_zelle.amount = total
            solicitud_zelle.save()
            carro = Carro(request)
            carro.limpiar_carro()

            context = {
                "total": total,
                "products": products,
            }
            html_message = render_to_string('purchases/email/email_template.html', context)
            plain_message = strip_tags(html_message)
            subject_email = "Solicitud de compra con E-commerce con éxito"
            user_email = solicitud_zelle.email

            send_mail(
                subject=subject_email,
                message=plain_message,
                from_email=EMAIL_HOST_USER,
                recipient_list=[user_email],
                html_message=html_message,
                fail_silently=False,
            )
            return redirect('purchases:ver_solicitud', id_solicitud=solicitud_zelle.pk)
    else:
        form = SolicitudZelleForm(user=request.user)

    return render(request, 'purchases/crear_solicitud_zelle.html', {'form': form})



@login_required
def view_solicitud_zelle(request, id_solicitud):
    solicitud = get_object_or_404(SolicitudZelle, id=id_solicitud)

    # Check if the user has permission to view the solicitud
    if request.user != solicitud.user and request.user.usuario.rol.nombre != 'admin':
        return render(request, 'error.html', {'error_message': 'No tienes permiso para ver esta solicitud.'}, status=403)

    # Get the SolicitudZelleItem objects associated with the solicitud

    solicitud_items = SolicitudZelleItem.objects.filter(solicitud=solicitud)



    context = {
        'solicitud': solicitud,
        'solicitud_items': solicitud_items,
    }

    return render(request, 'purchases/ver_solicitud_zelle.html', context)




def solicitud_list(request):
    # Obtener los parámetros de filtro de la solicitud

    filter_usuario = request.GET.get('usuario' or None)

    if request.user.usuario.rol.nombre == 'admin':



        # Filtrar las solicitudes en base a los parámetros
        if filter_usuario:
            solicitudes = SolicitudZelle.objects.filter(user__username__icontains=filter_usuario)
        else:
            solicitudes = SolicitudZelle.objects.all()
    else:
        solicitudes = SolicitudZelle.objects.filter(user=request.user)



    filter_estado = request.GET.get('estado')
    if filter_estado:
        solicitudes = solicitudes.filter(status=filter_estado)
    else:
        solicitudes = solicitudes.order_by('-status', '-id')

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
        'solicitudes': page_solicitudes,
        'filter_usuario': filter_usuario,
        'filter_estado': filter_estado
    }
    return render(request, 'purchases/solicitud_list.html', context)


@role_required(['admin'])
def aceptar_solicitud(request,id_solicitud):
    solicitud = get_object_or_404(SolicitudZelle, id=id_solicitud)
    solicitud.accept()

    context = {
        "id": id_solicitud,
    }
    html_message = render_to_string('purchases/email/solicitud_aceptada.html', context)
    plain_message = strip_tags(html_message)
    subject_email = "Solicitud de compra con E-commerce aceptada con éxito"
    user_email = solicitud.email

    send_mail(
        subject=subject_email,
        message=plain_message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[user_email],
        html_message=html_message,
        fail_silently=False,
    )
    return redirect('purchases:solicitud_list')


@role_required(['admin'])
def cancelar_solicitud(request,id_solicitud):
    solicitud = get_object_or_404(SolicitudZelle, id=id_solicitud)

    context = {
        "id": id_solicitud,
    }
    html_message = render_to_string('purchases/email/solicitud_rechazada.html', context)
    plain_message = strip_tags(html_message)
    subject_email = "Solicitud de compra con E-commerce rechazada"
    user_email = solicitud.email

    send_mail(
        subject=subject_email,
        message=plain_message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[user_email],
        html_message=html_message,
        fail_silently=False,
    )

    solicitud.cancel()
    return redirect('purchases:solicitud_list')









