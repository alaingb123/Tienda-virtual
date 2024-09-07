from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

from usuario.models import Rol,Usuario

# Register your models here.




@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    pass

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol')



User = get_user_model()
admin.site.unregister(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_active', 'is_staff', 'date_joined')  # Añade is_active aquí
    list_filter = ('is_active', 'is_staff')  # Filtros en el panel de administración

# Registra el modelo con la clase personalizada
admin.site.register(User, CustomUserAdmin)