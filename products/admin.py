from django.contrib import admin

# Register your models here.

from .models import Product,ProductImage,Clasificacion

admin.site.register(Product)

admin.site.register(ProductImage)
admin.site.register(Clasificacion)
