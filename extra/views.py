from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from extra.forms import DestinatarioForm
from extra.models import Destinatario
from products.models import Product


# Create your views here.



def crear_destinatario(request):
    if request.method == 'POST':
        form = DestinatarioForm(request.POST)
        if form.is_valid():
            destinatario = form.save(commit=False)
            destinatario.usuario = request.user  # Asignar el usuario actual
            destinatario.save()
            return redirect('extra:list_destinatario')
    else:
        form = DestinatarioForm()
    return render(request, 'extra/crear_destinatario.html', {'form': form})


def lista_destinatarios(request):
    """Vista para mostrar la lista de destinatarios."""
    destinatarios = Destinatario.objects.filter(usuario=request.user)  # Filtra por usuario actual
    query = request.GET.get('q')  # Obtiene el término de búsqueda de la URL
    print(query)
    if query:
        destinatarios = destinatarios.filter(nombre__icontains=query)
    else:
        pass

    session = request.session
    carro = session.get('carro', {})
    stock_error_products = []

    for item_id, item in carro.items():
        product = get_object_or_404(Product, pk=item["product_id"])
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



    context = {
        'destinatarios': destinatarios
    }

    return render(request, 'extra/list_destinatarios.html',context )

def editar_destinatario(request, destinatario_id):
    destinatario = Destinatario.objects.get(pk=destinatario_id)

    if request.method == 'POST':
        form = DestinatarioForm(request.POST, instance=destinatario)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("extra:list_destinatario"))  # Redirige a la lista de destinatarios
    else:
        form = DestinatarioForm(instance=destinatario)

    return render(request, 'extra/editar_destinatario.html', {'form': form})

