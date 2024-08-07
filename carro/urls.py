from django.urls import path

from . import views

app_name = 'carro'
urlpatterns = [
    path('agregar/<int:product_id>/', views.agregar_producto, name='agregar'),
    path('eliminar/<int:product_id>/', views.eliminar_producto, name='eliminar'),
    path('restar/<int:product_id>/', views.restar_producto, name='restar'),
    path('limpiar/', views.limpiar_carro, name='limpiar'),

]