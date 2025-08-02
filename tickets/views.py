from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Ticket
from ticketsadmin.models import Empresa, Anuncios
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Create your views here.

def home(request):
    holding = Empresa.objects.first()
    if not holding:
        return HttpResponse("No hay información de la empresa disponible.")
    informaciones = Anuncios.objects.filter(is_activo=True)
    return render(request, 'home.html', {'title': 'Tickets', 'message': 'Sistema de Ingreso de Tickets',
                                                   'empresa': holding.nombre_empresa,
                                                   'anuncios': informaciones})

def login(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('Dashboard Page')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos!','form': AuthenticationForm()})
    else:
        return render(request, 'login.html', {'message': 'Ingresa tus datos!',
                                              'titulo': 'Acceso al Sistema',
                                               'form': AuthenticationForm()})
    
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Dashboard Page')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form, 'message': 'Regístrate para acceder al sistema'})
