from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models

# Create your models here.

class Rol(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario')
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='usuarios', null=True)

    def __str__(self):
        return self.user.username
