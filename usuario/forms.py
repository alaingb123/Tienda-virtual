from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms


# input_css_class = "form-control"
class CrearUsuarioFormulario(UserCreationForm):
    email = forms.EmailField(required=True)  # Campo obligatorio

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise ValidationError("Por favor, utiliza un correo de Gmail.")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está en uso.")
        return email







class PerfilUsuarioFormulario(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class FormularioActualizarUsuario(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(FormularioActualizarUsuario, self).__init__(*args, **kwargs)
        for field in self.fields:
            # Añadir clases CSS a cada campo
            self.fields[field].widget.attrs.update({
                'class': 'input',  # Clase para aplicar estilos
                'placeholder': field.label,  # Placeholder con el nombre del campo
                'style': 'border: 1px solid var(--davys-gray); border-radius: 5px; padding: 10px; width: 100%; height: 3rem; font-size: 1em; transition: border-color 0.3s;'
            })