from django.contrib import admin
from django.urls import path
from online import views
from online.views import Index, RegisterView, LoginView, foro_view, perfil
from administracion.views import GestionUsuarios, EliminarUsuario
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index),
    path('Login/', LoginView.as_view(), name='Login'),
    path('Register/', RegisterView.as_view(), name='Register'),
    path('Logout/', LogoutView.as_view(next_page='/Login/'), name='Logout'),
    path('GestionUsuarios/', GestionUsuarios),
    path('EliminarUsuario/<int:idUser>', EliminarUsuario),
    path('perfil/', perfil, name='perfil'),
    path('contacto/', views.contacto, name='contacto'),
    path('foros/', views.foro_view, name='listar_foros'),  # Lista de foros
    path('foros/<int:foro_id>/', views.foro_view, name='ver_foro'),  # Ver foro específico
    path('crear/', views.crear_foro, name='crear_foro'),
]
