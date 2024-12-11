from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime
from online.forms import ForoForm, RegisterForm, LoginForm
from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from online.models import Foro, Usuario, Respuesta
from django.contrib import messages


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'Register.html'
    success_url = '/Login/'

    def form_valid(self, form):
        user = form.save()
        return redirect(self.success_url)

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/'  # Redirige a la página principal (index.html)
    success_message = "%(name)s Se ha creado exitosamente!"

    def form_valid(self, form):
        request = self.request
        usuario = form.cleaned_data.get("Usuario")
        password = form.cleaned_data.get("password")
        remember_me = form.cleaned_data['remember_me']
        user = authenticate(request, username=usuario, password=password)
        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            # Redirige al index.html después de iniciar sesión
            return redirect('/')
        return super(LoginView, self).form_invalid(form)

def Index(request):
    return render(request, "index.html")

@login_required
def perfil(request):
    usuario = request.user  # Obtenemos el usuario logeado
    if request.method == "POST":
        # Actualizamos los campos según los datos del formulario
        usuario.usuario = request.POST.get('usuario')
        usuario.correo = request.POST.get('correo')
        usuario.rut = request.POST.get('rut')
        usuario.telefono = request.POST.get('telefono')

        # Guardar los cambios en la base de datos
        usuario.save()
        messages.success(request, "¡Tu perfil ha sido actualizado exitosamente!")
        return redirect('perfil')  # Redirige al mismo perfil para ver los cambios

    return render(request, "perfil.html", {"usuario": usuario})

def contacto(request):
    return render(request, 'contacto.html')  # Asegúrate de que el archivo contacto.html exista


from django.shortcuts import render, get_object_or_404, redirect
from .models import Foro, Respuesta
from .forms import RespuestaForm

def foro_view(request, foro_id=None):
    if foro_id:
        # Mostrar un foro específico
        foro = get_object_or_404(Foro, id=foro_id)
        respuestas = foro.respuestas.all()

        # Procesar el formulario de respuesta
        if request.method == 'POST':
            form = RespuestaForm(request.POST)
            if form.is_valid():
                respuesta = form.save(commit=False)
                respuesta.autor = request.user  # Asignar el usuario actual como autor de la respuesta
                respuesta.foro = foro  # Asociar la respuesta al foro
                respuesta.save()
                return redirect('ver_foro', foro_id=foro.id)
        else:
            form = RespuestaForm()

        return render(request, 'foros.html', {
            'foro': foro,
            'respuestas': respuestas,
            'form': form,
            'modo': 'ver_foro'
        })
    else:
        # Listar todos los foros
        foros = Foro.objects.all()
        return render(request, 'foros.html', {'foros': foros, 'modo': 'listar_foros'})


def crear_foro(request):
    if request.method == 'POST':
        form = ForoForm(request.POST)
        if form.is_valid():
            # Asignar el usuario que está creando el foro
            nuevo_foro = form.save(commit=False)
            nuevo_foro.creador = request.user
            nuevo_foro.save()
            return redirect('listar_foros')  # O redirigir al foro creado, según lo que desees
    else:
        form = ForoForm()
    
    return render(request, 'crear_foro.html', {'form': form})
