from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario
from tickets.models import cargos,areas

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su usuario'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'})) 
    error_messages = {
        'invalid_login': {
            'message': "Por favor, ingrese un usuario y contraseña válidos.",
        },
    }   

class RegistroForm(UserCreationForm):
    id_area = forms.ModelChoiceField(
    queryset=areas.objects.filter(is_activo=True),
    widget=forms.Select(attrs={'class':'form-control'}),
    label='Área',
    empty_label='Seleccione Área'
    )
    id_cargo = forms.ModelChoiceField(
    queryset=cargos.objects.none(),
    widget=forms.Select(attrs={'class':'form-control'}),
    label='Cargo',
    empty_label='Seleccione Cargo',
    required=False
    )
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'}))
    password2 = forms.CharField(label='Confirme Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita su contraseña'}))

    class Meta(UserCreationForm.Meta):
        # El modelo que se usará para el formulario
        model = Usuario
        # Los campos que se mostrarán en el formulario
        fields = ('username', 'first_name', 'last_name','apodo', 'email', 'image_perfil','id_area','id_cargo', 'password1', 'password2')

        # Personalización de widgets, labels y help_texts para los campos
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su usuario'}),
            'apodo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Apodo'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sus Apellidos'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'image_perfil': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        
        labels = {
            'username': 'Usuario',
            'apodo':'Apodo',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo Electrónico',
            'image_perfil': 'Imagen Perfil',
            'id_area': 'Àrea',
            'id_cargo': 'Cargo',
            'password1': 'Contraseña',
            'password2': 'Confirme Contraseña',
        }
        
        help_texts = {
            'username': 'Requerido. 30 caracteres o menos. Letras, números y @/./+/-/_ solamente.',
            'apodo': 'Requerido, 20 carácteres sólo letras y números',
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
    
    def clean_apodo(self):
        apodo = self.cleaned_data.get('apodo')
        if len(apodo) > 20:
            raise forms.ValidationError("El nombre de usuario no puede tener más de 20 caracteres.")
                
            # Validar que solo sean letras y minúsculas
        if not apodo.islower() or not apodo.isalpha():
            raise forms.ValidationError("El Apodo contener solo letras minúsculas.")
        
        if Usuario.objects.filter(username=apodo).exists():
            raise forms.ValidationError("Este Apodo  ya está en uso.")
        return apodo
        
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
    id_area = forms.ModelChoiceField(
        queryset=areas.objects.filter(is_activo=True, cargos__isnull=False).distinct(),
        widget=forms.Select(attrs={'class':'form-control'}),
        label='Áreas',
        empty_label='Seleccione Área'
    )
    
    id_cargo = forms.ModelChoiceField(
        queryset=cargos.objects.filter(is_activo=True),
        widget=forms.Select(attrs={'class':'form-control'}),
        label='Cargo',
        empty_label='Seleccione Cargo'
    )
    
    # Campo de contraseña opcional, se hará visible en __init__
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Contraseña',
        required=False  # Crucial para que no sea un campo obligatorio
    )
    is_admin = forms.BooleanField(
        label='Administrador',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    crea_ticket = forms.BooleanField(
        label='Crear Ticket',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Usuario
        # Nota: 'password' no está en fields aquí. Lo agregaremos dinámicamente.
        fields = ('apodo', 'first_name', 'last_name', 'email', 'image_perfil', 'id_area', 'id_cargo','date_of_birth')
        
        widgets = {
            'apodo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Apodo', 'required': True}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sus Apellidos', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Correo', 'required': True}),
            'image_perfil': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        
        labels = {
            'apodo':'Apodo',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo Electrónico',
            'image_perfil': 'Imagen Perfil',
            'id_area': 'Área',
            'id_cargo': 'Cargo',
            'date_of_birth': 'Fecha de Nacimiento',
        }
        
    def __init__(self, *args, **kwargs):
        # extrae el usuario que está viendo la página
        user_request = kwargs.pop('user', None)
        
        # Llama al constructor de la clase base
        super(EditFormUser, self).__init__(*args, **kwargs)
        
        if user_request and user_request.is_admin:
            self.fields['is_admin'].initial = self.instance.is_admin
            self.fields['is_admin'].required = False
            self.fields['crea_ticket'].initial = self.instance.crea_ticket
            self.fields['crea_ticket'].required = False
            self.fields['password'].required = False 
        else:
            del self.fields['password'] # Elimina el campo si no es admin
            del self.fields['is_admin'] # Elimina el campo si no es admin
            del self.fields['crea_ticket'] # Elimina el campo si no es admin

    def clean_apodo(self):
        apodo = self.cleaned_data.get('apodo')
        if self.instance.username != apodo and Usuario.objects.filter(username=apodo).exists():
            raise forms.ValidationError("Este Apodo ya está en uso.")
        # La validación de longitud y solo letras es mejor hacerla a nivel de modelo
        return apodo
            
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance.email != email and Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password) # Usa set_password para hashear la contraseña
        
        if 'is_admin' in self.fields:
            user.is_admin = self.cleaned_data.get('is_admin', False)

        if 'crea_ticket' in self.fields:
            user.crea_ticket = self.cleaned_data.get('crea_ticket',False)

        if commit:
            user.save()
        return user
    

class BuscarUsuarioForm(forms.Form):
    username = forms.CharField(
        label='Usuario, apodo o nombre',
        max_length=50,
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de Usuario, apodo o nombre'})
    )
    area = forms.ModelChoiceField(
        queryset=areas.objects.all(),
        required=False,
        label='Área'
    )

    