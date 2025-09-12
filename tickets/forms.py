from django.forms import ModelForm
from django import forms
from .models import Ticket, MensajesTicket, RespuestaMensajeTicket, nivel, areas
from usuarios.models import Usuario

class TicketForm(ModelForm):
    id_cargo = forms.ModelChoiceField(
    queryset=nivel.objects.filter(is_activo=True),
    widget=forms.Select(attrs={'class':'form-control'}),
    label='Nivel',
    empty_label='Seleccione Nivel'
    )
    id_area = forms.ModelChoiceField(
    queryset=areas.objects.filter(is_activo=True),
    widget=forms.Select(attrs={'class':'form-control','required':True}),
    label='Área',
    empty_label='Seleccione Área'
    )

    class Meta:
        model = Ticket
        fields = ['titulo', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control','required':True}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control','required':True}),

        }
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'id_nivel': 'Nivel',
        }
        help_texts = {
            'title': 'Ingrese el título de la tarea.',
            'description': 'Ingrese una descripción detallada de la tarea.',
        }
        error_messages = {
            'title': {
                'max_length': 'El título no puede exceder los 100 caracteres.',
            },
            'description': {
                'required': 'La descripción es opcional, pero si se proporciona, debe ser breve.',
            },
        }
        
class MesnsajeForm(ModelForm):
    class Meta:
        model: MensajesTicket
        fields=['mensaje']
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows':4, 'cols':40, 'class': 'form-control','required':True}),
        }
        labels = {
            'mensaje': 'Mensaje',
        }
        help_texts = {
            'mensaje': 'Mensaje Mínimo esperado OK'
        }
        error_messages = {
            'title': {
                'min_lengh': 'El Mensaje mínimo debe ser 2 caracteres',
                'max_length': 'El Mensaje no puede exceder los 100 caracteres.',
            }
        }

class RespuestaFrom(ModelForm):
    class Meta:
        model: RespuestaMensajeTicket
        fields=['respuesta']
        widgets = {
            'respuesta': forms.Textarea(attrs={'rows':4, 'cols':40, 'class': 'form-control'}),
        }
        labels = {
            'respuesta': 'Respuesta',
        }
        help_texts = {
            'mensaje': 'Mínima respuesta esperada OK'
        }
        error_messages = {
            'title': {
                'min_lengh': 'La Respuesta debe ser 2 caracteres',
                'max_length': 'La Respuesta no puede exceder los 100 caracteres.',
            }
        }

class AsignarForm(ModelForm):
    asignado_a = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(is_active=True,is_superuser=False),
        widget=forms.Select(attrs={'class': 'form-control', 'required': True}),
        label='Asignar a',
        empty_label='Seleccione Usuario'
    )
    
    # También, es redundante definir estos campos si ya están en Meta
    id_nivel = forms.ModelChoiceField(
        queryset=nivel.objects.filter(is_activo=True),
        widget=forms.Select(attrs={'class':'form-control'}),
        label='Nivel',
        empty_label='Seleccione Nivel'
    )

    def __init__(self, *args, **kwargs):
        # Es mejor usar .pop() para eliminar 'user' del diccionario de kwargs
        # antes de pasarlo al constructor de la clase padre.
        user = kwargs.pop('user', None)
        # Super() debe ir antes de modificar el campo para que el formulario se inicialice
        super().__init__(*args, **kwargs)
        
        if user: 
            self.fields['asignado_a'].queryset = Usuario.objects.filter(
                is_active=True, is_superuser=False
            ).exclude(id=user.id)
    
    class Meta:
        model = Ticket
        fields = ['asignado_a', 'id_nivel']

        labels = {
            'asignado_a': 'Asignar a',
            'id_nivel': 'Nivel',
        }

        help_texts = {
            'asignado_a': 'Seleccione el usuario al que desea asignar el ticket.',
            'id_nivel': 'Seleccione el nivel del ticket.',
        }
        error_messages = {
            'asignado_a': {
                'required': 'Debe seleccionar un usuario para asignar el ticket.',
            }
        }

class RevisaTicketForm(ModelForm):
    # Definimos los campos de relación explícitamente.
    # No necesitan un queryset porque solo vamos a mostrar sus valores.
    id_nivel_nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),
        label='Nivel'
    )
    id_area_nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': True}),
        label='Área'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        
        if instance:
            self.fields['id_nivel_nombre'].initial = instance.id_nivel.nombre
            self.fields['id_area_nombre'].initial = instance.id_area.nombre

    class Meta:
        model = Ticket
        # Los campos de Meta deben ser campos directos del modelo.
        fields = ['titulo', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'readonly': True}),
        }
        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
        }
        error_messages = {
            'titulo': {'max_length': 'El título no puede exceder los 100 caracteres.'},
            'descripcion': {'required': 'La descripción es opcional, pero si se proporciona, debe ser breve.'},
        }

class BusquedaAsignacion(forms.Form):
    ticket= forms.CharField(
        label='Numero de Ticket o Título',
        max_length=50,
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el ID del Ticket o Título'})
    )

