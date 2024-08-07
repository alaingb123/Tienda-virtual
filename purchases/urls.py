from django.urls import path

from . import views

app_name='purchases'
urlpatterns = [

    path('success/', views.purchase_success_view, name='success'),
    path('success_cart/', views.purchase_success_cart_view, name='success_cart'),
    path('stopped/', views.purchase_stopped_view, name='stopped'),
    path('cart/', views.cart, name='cart'),

    
    # Compra con stripe
    path('start/', views.purchase_start_view, name='start'),
    path('buy_cart/', views.buy_cart, name='buy_cart'),

    # COmpra con zelle
    path('create_solicitud_zelle/', views.create_solicitud_zelle, name='create_solicitud_zelle'),
    path('ver_solicitud/<int:id_solicitud>', views.view_solicitud_zelle, name='ver_solicitud'),
    path('list_solicitud/', views.solicitud_list, name='solicitud_list'),
    path('aceptar_solicitud/<int:id_solicitud>', views.aceptar_solicitud, name='aceptar_solicitud'),
    path('cancelar_solicitud/<int:id_solicitud>', views.cancelar_solicitud, name='cancelar_solicitud'),
]