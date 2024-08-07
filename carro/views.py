from django.http import JsonResponse
from django.shortcuts import render,redirect
from .carro import Carro
from products.models import Product

def agregar_producto(request,product_id):
    carro = Carro(request)
    product = Product.objects.get(pk=product_id)

    quantity = int(request.POST.get('quantity', 1))
    print(" la cantidad es : ", quantity)
    carro.agregar(product=product,quantity=quantity)

    return redirect("products:list")


# def agregar_producto(request,product_id):
#     carro = Carro(request)
#     product = Product.objects.get(pk=product_id)
#
#     quantity = int(request.POST.get('quantity', 1))
#     print(" la cantidad es : ", quantity)
#     carro.agregar(product=product,quantity=quantity)
#
#     return JsonResponse(carro.carro)



def restar_producto(request, product_id):
    carro = Carro(request)
    product = Product.objects.get(pk=product_id)

    carro.restar_product(product=product)

    return redirect("products:list")


def limpiar_carro(request):
    carro = Carro(request)

    carro.limpiar_carro()

    return redirect("products:list")

def eliminar_producto(request,product_id):
    carro = Carro(request)
    product = Product.objects.get(pk=product_id)
    carro.eliminar(product)

    return redirect("products:list")









