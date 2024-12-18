from django import forms
from online.models import Foro, Respuesta, Usuario

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    password_2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'}))
    telefono = forms.CharField(label='', max_length=15, required=False, 
                               widget=forms.TextInput(attrs={'placeholder': 'Número de teléfono (opcional)'}))
    
    class Meta:
        model = Usuario
        fields = ['usuario', 'correo', 'rut', 'telefono']
        widgets = {
            'correo': forms.TextInput(attrs={'placeholder': 'Ingrese su correo'}),
            'usuario': forms.TextInput(attrs={'placeholder': 'Ingrese su usuario'}),
            'rut': forms.TextInput(attrs={'placeholder': 'Ingrese su rut'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        usuario = cleaned_data.get("usuario")

        if len(usuario) > 20:
            self.add_error("usuario", "El nombre de usuario es demasiado largo!")
        if len(password) == 0:
            self.add_error("usuario", "Debe ingresar un nombre de usuario!")
        if len(password) < 8:
            self.add_error("password", "La contraseña debe ser mayor a 8 dígitos")
        if password is not None and password != password_2:
            self.add_error("password_2", "Las contraseñas no coinciden")
        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["password"])
        if commit:
            usuario.save()
        return usuario

class LoginForm(forms.Form):
    Usuario = forms.CharField(label='', max_length=63, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su usuario'}))
    password = forms.CharField(label='', max_length=63, widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña'}))
    remember_me = forms.BooleanField(label='Recordar contraseña', required=None)

class ForoForm(forms.ModelForm):
    class Meta:
        model = Foro
        fields = ['titulo', 'descripcion']

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ['contenido']
