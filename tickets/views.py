from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Ticket
from ticketsadmin.models import Empresa, Anuncios
from usuarios.forms import LoginForm, RegistroForm


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
    if request.user.is_authenticated:
        return redirect('Dashboard Page')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('Dashboard Page')
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Usuario o contraseña incorrectos!'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'message': 'Ingresa tus datos!', 'titulo': 'Acceso al Sistema'})


    
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Dashboard Page')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form, 
                                             'titulo': 'Registro de Usuario',
                                             'message': 'Regístrate para acceder al sistema',
                                             'error': ''})

@login_required
def logout(request):
    logout(request)
    return redirect('Home Page')

@login_required
def dashboard(request):
    tickets = Ticket.objects.all()
    return render(request, 'dashboard.html', {'tickets': tickets, 'title': 'Dashboard', 'message': 'Bienvenido al Dashboard'})
