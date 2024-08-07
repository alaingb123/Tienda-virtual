from django.contrib import admin
from django.contrib.auth.models import User, Group

from usuario.models import Rol,Usuario

# Register your models here.




@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    pass

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol')
