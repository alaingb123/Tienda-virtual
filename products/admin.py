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

@admin.register(ProductOffer)
class ProductOfferAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_active')

    actions = ['execute_update_offers']

    def execute_update_offers(self, request, queryset):
        for offer in queryset:
            offer.is_offer_active()
        self.message_user(request, "Ofertas actualizadas exitosamente.")

    execute_update_offers.short_description = "Actualizar ofertas"



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




