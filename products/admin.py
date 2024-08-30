from django.contrib import admin

# Register your models here.

from .models import Product, ProductImage, ClasificacionPadre, ClasificacionHija, ProductOffer, ClasificacionNieta, \
    Rating_product, Rating

admin.site.register(Product)
admin.site.register(ClasificacionNieta)

admin.site.register(ProductImage)


@admin.register(Rating_product)
class Rating_product(admin.ModelAdmin):
    list_display = ('product', 'average_rating')

@admin.register(Rating)
class Rating(admin.ModelAdmin):
    list_display = ('average', 'user', "score")



class ProductOfferAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_premium', 'is_active')
    search_fields = ('product__name',)  # Permite buscar por el nombre del producto
    fields = ('product', 'is_premium')  # Solo permitimos cambiar el producto y el campo is_premium
    readonly_fields = ('precio_nuevo', 'precio_viejo', 'start_date', 'end_date', 'is_active')  # Hacemos que los demás campos sean de solo lectura
    actions = ['execute_update_offers']  # Registramos la acción personalizada

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def execute_update_offers(self, request, queryset):
        for offer in queryset:
            offer.is_offer_active()  # Asegúrate de que esta función esté definida en tu modelo
        self.message_user(request, "Ofertas actualizadas exitosamente.")

    execute_update_offers.short_description = "Actualizar ofertas"

admin.site.register(ProductOffer, ProductOfferAdmin)





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




from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Personalizar el título del admin
admin.site.site_header = _("Administración de E-commerce")
admin.site.site_title = _("E-commerce")
admin.site.index_title = _("Bienvenido al panel de administración de E-Commerce")