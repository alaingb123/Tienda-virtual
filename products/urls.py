from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    path('create/', views.product_create_view, name='create'),
    path('mis_productos_table/', views.mis_productos_table, name='mis_productos'),
    path('', views.product_list_view, name='list'),

    path('<slug:handle>/', views.product_detail_view, name='detail'),
    path('<slug:handle>/manage/', views.product_manage_detail_view, name='manage'),
    path('<slug:handle>/download/<int:pk>', views.product_attachment_download_view, name='download'),

    path('search/', views.search, name='search'),

    # path('eliminar/<slug:handle>/', views.delete_product, name='eliminar'),



]
