from django.forms import ModelForm
from django import forms
from .models import Ticket    

class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['titulo', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Título',
            'description': 'Descripción',
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
        # Add any additional customization as needed