from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su usuario'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'})) 
    error_messages = {
        'invalid_login': {
            'message': "Por favor, ingrese un usuario y contraseña válidos.",
        },
    }   

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username','first_name','last_name', 'image_perfil','password1', 'password2', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su email'}),
            'image_perfil': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme su contraseña'}),
        },
        labels = {
            'username': 'Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Email',
            'image_perfil': 'Imagen de Perfil',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña',
        },
        help_texts = {
            'username': 'Requerido. 20 caracteres o menos. Letras, números y @/./+/-/_ solamente.',
            'password1': 'Ingrese una contraseña segura.',
        },
        error_messages = {
            'username': {
                'max_length': "El usuario no puede tener más de 20 caracteres.",
                'unique': "Este usuario ya está registrado.",
            },
            'email': {
                'unique': "Este email ya está registrado.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'autocomplete': 'new-password'})
        self.fields['password2'].widget.attrs.update({'autocomplete': 'new-password'})

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2
            
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError("Este usuario ya está registrado.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True  # Activar el usuario al registrarse
        if commit:
            user.save()
        return user     
