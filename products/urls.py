from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    path('create/', views.product_create_view, name='create'),
    path('mis_productos_table/', views.mis_productos_table, name='mis_productos'),
    path('', views.product_list_view, name='list'),
    path('filter/<int:provider_id>/', views.product_list_view, name='filter_by_provider'),


    path('<slug:handle>/', views.product_detail_view, name='detail'),
    path('<slug:handle>/manage/', views.product_manage_detail_view, name='manage'),
    path('<slug:handle>/download/<int:pk>', views.product_attachment_download_view, name='download'),

    path('search/', views.search, name='search'),

    # path('eliminar/<slug:handle>/', views.delete_product, name='eliminar'),


    #Crear oferta
    path('crear_oferta/<int:product_id>/', views.crear_oferta, name='crear_oferta'),
    path('eliminar_oferta/<int:product_id>/', views.eliminar_oferta, name='eliminar_oferta'),
    path('rate_product/<int:product_id>/', views.rate_product, name='rate_product'),

]
