from ftplib import MAXLINE
from django import forms
from .models import Producto, Usuario
from django.contrib.auth.forms import UserChangeForm


class Login(forms.Form):
    correo = forms.EmailField(label='Correo', max_length=200, widget=forms.EmailInput(attrs={'placeholder': 'Ingrese su correo', 'class' : 'inputL'}))
    contraseña = forms.CharField(label='Contraseña', max_length=200, widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña', 'class' : 'inputL'}))

class Register(forms.Form):
    username = forms.CharField(label='Nombre', max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre', 'class' : 'inputR'}))
    correo = forms.EmailField(label='Correo', max_length=200, widget=forms.EmailInput(attrs={'placeholder': 'Ingrese su correo', 'class' : 'inputR'}))
    contraseña = forms.CharField(label='Contraseña', max_length=200, widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña', 'class' : 'inputR'}))
    contraseña2 = forms.CharField(label='Repetir Contraseña', max_length=200, widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña', 'class' : 'inputR'}))

class Product(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'cantidad', 'imagen1', 'imagen2', 'imagen3', 'imagen4', 'imagen5', 'especificaciones']
        
        # Aquí puedes personalizar los widgets si es necesario
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre', 'class' : 'inputP'}),
            'descripcion': forms.TextInput(attrs={'placeholder': 'Ingrese la descripción', 'class' : 'inputP'}),
            'precio': forms.NumberInput(attrs={'placeholder': 'Ingrese el precio', 'class' : 'inputP'}),
            'cantidad': forms.NumberInput(attrs={'placeholder': 'Ingrese la cantidad', 'class' : 'inputP'}),
            'imagen1': forms.FileInput(attrs={'class' : 'inputP'}),
            'imagen2': forms.FileInput(attrs={'class' : 'inputP'}),
            'imagen3': forms.FileInput(attrs={'class' : 'inputP'}),
            'imagen4': forms.FileInput(attrs={'class' : 'inputP'}),
            'imagen5': forms.FileInput(attrs={'class' : 'inputP'}),
            'especificaciones': forms.TextInput(attrs={'placeholder': 'Ingrese las especificaciones', 'class' : 'inputP'}),
        }

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['foto_perfil', 'username', 'email', 'biografia']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nombre de usuario', 'class': 'username-class'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico', 'class': 'email-class'}),
            'biografia': forms.Textarea(attrs={'placeholder': 'Escribe una biografía', 'class': 'biografia-class'}),
        }

class UsuarioChangeForm(UserChangeForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput, required=False)

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'foto_perfil', 'biografia', 'is_superuser', 'is_staff', 'is_active', 'last_login', 'date_joined']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'foto_perfil': 'Foto de perfil',
            'biografia': 'Biografía',
            'is_superuser': 'Estado de superusuario',
            'is_staff': 'Estado de personal',
            'is_active': 'Activo',
            'last_login': 'Último inicio de sesión',
            'date_joined': 'Fecha de registro'
        }
        help_texts = {
            'password': 'Las contraseñas no se almacenan en texto claro, por lo que no hay forma de ver la contraseña del usuario.',
            'is_superuser': 'Designa si este usuario tiene todos los permisos sin necesidad de asignarlos explícitamente.',
            'is_staff': 'Designa si este usuario puede iniciar sesión en el sitio de administración.',
            'is_active': 'Designa si este usuario debe ser tratado como activo. Desmarque esta opción en lugar de eliminar cuentas.'
        }
