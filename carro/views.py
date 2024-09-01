from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .carro import Carro
from products.models import Product

def agregar_producto(request,product_id):
    carro = Carro(request)
    product = Product.objects.get(pk=product_id)
    if product.active == False:
        return redirect('products:list')
    quantity = int(request.POST.get('quantity', 1))
    print(" la cantidad es : ", quantity)
    carro.agregar(product=product,quantity=quantity)


    return redirect("products:list")


def agregar_producto_desde_carro(request,product_id):
    carro = Carro(request)
    product = Product.objects.get(pk=product_id)

    quantity = int(request.POST.get('quantity', 1))
    print(" la cantidad es : ", quantity)
    carro.agregar(product=product, quantity=quantity)

    return redirect("carro:ver_carro")





def restar_producto(request, product_id):
    carro = Carro(request)
    product = Product.objects.get(pk=product_id)

    carro.restar_product(product=product)

    return redirect("carro:ver_carro")


def limpiar_carro(request):
    carro = Carro(request)

    carro.limpiar_carro()

    return redirect("carro:ver_carro")

def eliminar_producto(request,product_id):
    carro = Carro(request)
    product = Product.objects.get(pk=product_id)
    carro.eliminar(product)

    return redirect("carro:ver_carro")


def ver_carro(request):
    session = request.session
    carro = session.get('carro', {})
    stock_error_products = []
    stock_error = None

    for item_id, item in carro.items():
        try:
            product = get_object_or_404(Product, pk=item["product_id"])
            if product.supply < item["cantidad"] or not product.active:
                stock_error_products.append(product.name)
        except:
            pass

    if stock_error_products:
        stock_error = "Lo sentimos, no hay suficiente disponibilidad de los siguientes productos: " + ", ".join(stock_error_products) + ". Te recomendamos que los retires del carrito para continuar con tu compra."

    context = {
        "stock_error": stock_error
    }
    return render(request, "purchases/cart.html", context)






