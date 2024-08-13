from django.contrib import admin

# Register your models here.

from .models import Product, ProductImage, ClasificacionPadre, ClasificacionHija

admin.site.register(Product)

admin.site.register(ProductImage)



# Modelo ClasificacionPadre
@admin.register(ClasificacionPadre)
class ClasificacionPadreAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'num_hijos')
    search_fields = ('nombre',)

    def num_hijos(self, obj):
        return obj.hijos.count()

    num_hijos.short_description = 'Número de hijos'


# Modelo ClasificacionHija
@admin.register(ClasificacionHija)
class ClasificacionHijaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'padre')
    search_fields = ('nombre', 'padre__nombre')
    list_filter = ('padre',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('padre')