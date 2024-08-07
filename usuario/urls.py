


from django.urls import path

from usuario.views import crear_usuario, iniciar_sesion, editar_perfil, eliminar_usuario,cerrar_sesion,MyPasswordChangeView,password_change_done


app_name = 'usuario'
urlpatterns = [


        path('crear_usuario/', crear_usuario, name='create'),
        path('iniciar_sesion/', iniciar_sesion, name='login'),
        path('editar_perfil/', editar_perfil, name='update_user'),
        path('eliminar_usuario/', eliminar_usuario, name='eliminar_usuario'),
        path('cerrar_sesion/', cerrar_sesion, name='logout'),

        # Cambiar Contraseña
        path('password/', MyPasswordChangeView.as_view(),
             name='change_password'),
        path('pasword_change/', password_change_done, name='password_change_done'),

]