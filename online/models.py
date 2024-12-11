from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):
    def create_user(self, correo, usuario=None, password=None, fecha_nacimiento=None, nombre=None, apellido=None, rut=None, admin=False, tecnico=False, activo=True):
        if not correo:
            raise ValueError('Deben tener correos')
        if not usuario:  # Cambiado de 'Usuario' a 'usuario'
            raise ValueError('Deben tener nombres de usuario')
        user = self.model(
            correo=self.normalize_email(correo),
            usuario=usuario,
            nombre=nombre,
            apellido=apellido,
            rut=rut,
            fecha_nacimiento=fecha_nacimiento,
        )
        user.set_password(password)  # Asegúrate de usar set_password
        user.admin = admin
        user.tecnico = tecnico
        user.activo = activo
        user.save()
        return user

    def create_superuser(self, correo, usuario, password=None, fecha_nacimiento=None, nombre=None, apellido=None, rut=None):
        user = self.create_user(
            correo=correo,
            usuario=usuario,
            password=password,
            nombre=nombre,
            apellido=apellido,
            rut=rut,
            admin=True,
            tecnico=False,
            activo=True,
        )
        user.save()
        return user

class Usuario(AbstractBaseUser):
    nombre = models.CharField(max_length=3, blank=True, null=True)
    apellido = models.CharField(max_length=30, blank=True, null=True)
    rut = models.CharField(max_length=12, unique=True)
    correo = models.EmailField(max_length=70, unique=True)
    usuario = models.CharField(max_length=50, unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)  # Campo para teléfono
    activo = models.BooleanField(default=True)
    admin = models.BooleanField(default=False) 
    tecnico = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['correo', 'rut']

    def get_full_name(self):
        return self.correo

    def get_short_name(self):
        return self.correo

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    objects = UserManager()

    @property
    def is_staff(self):
        return self.admin  # Cambiado a self.admin

    @property
    def is_admin(self):
        return self.admin

    def __str__(self):
        return self.usuario

class Foro(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="foros")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

# Modelo para las Respuestas del Foro
class Respuesta(models.Model):
    contenido = models.TextField()
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    foro = models.ForeignKey('Foro', related_name='respuestas', on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Respuesta de {self.autor.username} en {self.foro.titulo}"