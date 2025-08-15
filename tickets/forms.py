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