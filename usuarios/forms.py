from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su usuario'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'})) 
    error_messages = {
        'invalid_login': {
            'message': "Por favor, ingrese un usuario y contraseña válidos.",
        },
    }   

class RegistroForm(UserCreationForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'}))
    password2 = forms.CharField(label='Confirme Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita su contraseña'}))

    class Meta(UserCreationForm.Meta):
        # El modelo que se usará para el formulario
        model = Usuario
        # Los campos que se mostrarán en el formulario
        fields = ('username', 'first_name', 'last_name', 'email', 'image_perfil', 'password1', 'password2')

        # Personalización de widgets, labels y help_texts para los campos
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sus Apellidos'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'image_perfil': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        
        labels = {
            'username': 'Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo Electrónico',
            'image_perfil': 'Imagen Perfil',
            'password1': 'Contraseña',
            'password2': 'Confirme Contraseña',
        }
        
        help_texts = {
            'username': 'Requerido. 30 caracteres o menos. Letras, números y @/./+/-/_ solamente.',
            'password2':'Repita la contraseña'
        }

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 20:
            raise forms.ValidationError("El nombre de usuario no puede tener más de 20 caracteres.")
                
            # Validar que solo sean letras y minúsculas
        if not username.islower() or not username.isalpha():
            raise forms.ValidationError("El nombre de usuario debe contener solo letras minúsculas.")
        
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username
        

    def clean_email(self):
            email = self.cleaned_data.get('email')
            if Usuario.objects.filter(email=email).exists():
                raise forms.ValidationError("Este correo electrónico ya está en uso.")
            return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        if commit:
            user.save()
        return user

class EditFormUser(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('first_name','last_name','email','image_perfil')
        widgets = {
                'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}),
                'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sus Apellidos'}),
                'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ''}),
                'image_perfil': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            }
            
        labels = {
                'first_name': 'Nombre',
                'last_name': 'Apellidos',
                'email': 'Correo Electrónico',
                'image_perfil': 'Imagen Perfil',
            }
