from django.urls import path

from . import views

app_name='purchases'
urlpatterns = [




    #
    # # Compra con stripe
    # path('start/', viewsStripe.purchase_start_view, name='start'),
    # path('buy_cart/', viewsStripe.buy_cart_stripe, name='buy_cart'),
    # path('purchases_stripe/', viewsStripe.pedidos_stripe, name='purchases_stripe'),
    # path('ver_solicitud_stripe/<int:purchase_id>', viewsStripe.purchase_detail, name='ver_solicitud_stripe'),
    # path('success_cart/', viewsStripe.purchase_success_cart_view, name='success_cart'),
    # path('success/', viewsStripe.purchase_success_view, name='success'),
    # path('stopped/', viewsStripe.purchase_stopped_view, name='stopped'),

    # COmpra con zelle
    path('create_solicitud_zelle/', views.create_solicitud_zelle, name='create_solicitud_zelle'),
    path('ver_solicitud/<int:id_solicitud>', views.view_solicitud_zelle, name='ver_solicitud'),
    path('list_solicitud/', views.solicitud_list, name='solicitud_list'),
    path('aceptar_solicitud/<int:id_solicitud>', views.aceptar_solicitud, name='aceptar_solicitud'),
    path('cancelar_solicitud/<int:id_solicitud>', views.cancelar_solicitud, name='cancelar_solicitud'),
]