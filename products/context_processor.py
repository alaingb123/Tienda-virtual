from products.models import Product




def cantidad_like(request):
    liked_products = Product.objects.filter(like__user=request.user)
    cantidad_like = liked_products.count()
    return {'cantidad_like': cantidad_like}



