from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User



class CrearUsuarioFormulario(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs.update({'class':'form-control'})


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
            self.fields[field].widget.attrs.update({'class': 'form-control'})