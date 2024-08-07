from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth import login, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.cache import never_cache

from usuario.forms import CrearUsuarioFormulario, PerfilUsuarioFormulario
from django.core.mail import EmailMessage,send_mail


# Create your views here.


def crear_usuario(request):
    if request.method == 'POST':
        formulario = CrearUsuarioFormulario(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('usuario:login')  # Redirige al usuario a la página de inicio de sesión
    else:
        formulario = CrearUsuarioFormulario()

        for field in formulario.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })
    return render(request, 'usuario/create.html', {'form': formulario})



def iniciar_sesion(request):
    if request.method == 'POST':
        formulario = AuthenticationForm(request, data=request.POST)
        if formulario.is_valid():
            usuario = formulario.get_user()
            login(request, usuario)
            return redirect('products:list')  # Redirige al usuario a la página de inicio
        else:
            messages.error(request, 'El usuario o la contraseña es incorrecta')
    else:
        formulario = AuthenticationForm()

    for field in formulario.fields.values():
        field.widget.attrs.update({
            'class': 'form-control',
            'placeholder': field.label
        })
    return render(request, 'usuario/login.html', {'formulario': formulario})




@never_cache
@login_required
def editar_perfil(request):
    if request.method == 'POST':
        formulario = PerfilUsuarioFormulario(request.POST, instance=request.user)
        if formulario.is_valid():
            formulario.save()
            return redirect('products:list')  # Redirige al usuario a la página de perfil
    else:
        formulario = PerfilUsuarioFormulario(instance=request.user)

        for field in formulario.fields.values():
            field.widget.attrs.update({
                'placeholder': field.label
            })
    return render(request, 'usuario/update_user.html', {'form': formulario})


@login_required
@never_cache
def cerrar_sesion(request):
    logout(request)
    return redirect('usuario:login')





@login_required
def cambiar_contrasena(request):
    if request.method == 'POST':
        formulario = PasswordChangeForm(user=request.user, data=request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            update_session_auth_hash(request, usuario)  # Actualiza la sesión del usuario para evitar que se cierre la sesión
            messages.success(request, 'Tu contraseña ha sido actualizada.')
            return redirect('listar_clasificaciones')  # Redirige al usuario a la página de perfil
    else:
        formulario = PasswordChangeForm(user=request.user)

        for field in formulario.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })
    return render(request, 'usuario/change.html', {'formulario': formulario})



@login_required
def eliminar_usuario(request):
    # Obtén el usuario que desea eliminar
    usuario = get_object_or_404(User, id=request.user.id)

    usuario.delete()

        # Redirige a una página de éxito o cualquier otra acción que desees realizar después de eliminar al usuario
    return redirect('usuario:login')



class MyPasswordChangeView(PasswordChangeView):
    template_name = 'usuario/change_password.html'
    form_class = PasswordChangeForm
    success_url = '/usuario/pasword_change'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['old_password'].widget.attrs['class'] = 'form-control'
        form.fields['old_password'].widget.attrs['style'] = 'background-color: rgba(255,255,255,0)'
        form.fields['new_password1'].widget.attrs['class'] = 'form-control'
        form.fields['new_password1'].widget.attrs['style'] = 'background-color: rgba(255,255,255,0)'
        form.fields['new_password2'].widget.attrs['class'] = 'form-control'
        form.fields['new_password2'].widget.attrs['style'] = 'background-color: rgba(255,255,255,0)'
        return form



@login_required()
def password_change_done(request):
    return render(request, 'usuario/password_change_done.html')



