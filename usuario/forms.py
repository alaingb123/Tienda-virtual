from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


input_css_class = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
class CrearUsuarioFormulario(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = input_css_class





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
            self.fields[field].widget.attrs['class'] = input_css_class
