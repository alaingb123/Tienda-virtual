from django.db import models

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from carro.carro import Carro
from extra.models import Destinatario
from products.models import Product
from django.core.exceptions import PermissionDenied
from django.core.validators import EmailValidator,RegexValidator
import uuid

from django.conf import settings
from django.core.validators import EmailValidator, RegexValidator
# Create your models here.
import string
import random


def generate_unique_handle():
    while True:
        handle = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if not Purchase.objects.filter(handle=handle).exists():
            return handle




class Purchase(models.Model):
    ENTREGA_CHOICES = [
        ('pending', 'En espera'),
        ('onway', 'En camino'),
        ('accepted', 'Entregada'),
        ('canceled', 'Cancelada'),
    ]
    handle = models.CharField(max_length=6, unique=True, default=generate_unique_handle, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, related_name='pedidos_stripe')
    stripe_checkout_session_id = models.CharField(max_length=220, null=True, blank=True)
    completed = models.BooleanField(default=False)
    stripe_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)  # Campo para la cantidad de dinero
    timestamp = models.DateTimeField(auto_now_add=True)
    entrega = models.CharField(max_length=10, choices=ENTREGA_CHOICES,
                               default='pending')  # Campo para el estado de la solicitud
    destinatario = models.ForeignKey(Destinatario, on_delete=models.SET_NULL, null=True, blank=True)

    def guardar_producto(self,product,quantity,purchase):

        SolicitudStripeItem.objects.create(
            solicitud=purchase,
            product=product,
            quantity=quantity
        )

    def __str__(self):
        return f"{self.pk} - {self.user.username}"


# NEcesidad de crear un campo id que contenga letras
class SolicitudStripeItem(models.Model):
    handle = models.CharField(max_length=6, unique=True, default=generate_unique_handle, editable=False)
    solicitud = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"id:{self.pk} - Products:{self.product.name} - {self.quantity}"



