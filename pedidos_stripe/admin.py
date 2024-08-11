from django.contrib import admin

# Register your models here.

from .models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'stripe_checkout_session_id', 'completed', 'stripe_price', 'timestamp', 'entrega')
    list_filter = ('completed', 'timestamp', 'entrega')
    search_fields = ('user__username', 'product__name', 'stripe_checkout_session_id')
    readonly_fields = ('timestamp',)
