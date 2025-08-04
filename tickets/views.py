from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import IntegrityError
from .models import Ticket
from ticketsadmin.models import Empresa, Anuncios
from usuarios.forms import LoginForm, RegistroForm
from usuarios.models import Usuario


# Create your views here.

def home(request):
    holding = Empresa.objects.first()
    if not holding:
        return HttpResponse("No hay información de la empresa disponible.")
    informaciones = Anuncios.objects.filter(is_activo=True)
    return render(request, 'home.html', {'title': 'Tickets', 'message': 'Sistema de Ingreso de Tickets',
                                                   'empresa': holding.nombre_empresa,
                                                   'anuncios': informaciones})

def ingreso(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('Dashboard Page')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos!','form': LoginForm()})
    else:
        return render(request, 'login.html', {'message': 'Ingresa tus datos!',
                                               'form': LoginForm})

def registro(request):
    if request.method == 'POST':
        if request.POST['username'] and request.POST['password1'] and request.POST['password2'] and request.POST['email'] and request.POST['first_name'] and request.POST['last_name'] and request.POST['password2']:
            try:
                if request.POST['password1'] == request.POST['password2']:
                    user = Usuario.objects.create_user(
                        username=request.POST['username'],
                        password=request.POST['password1']
                    )
                    user.save()
                    login(request, user)
                    return redirect('Dashboard Page')
                else:
                    return render(request, 'registro.html', {'error': 'Contraseñas no coinciden!',
                                           'form': RegistroForm()}
                )
            except IntegrityError:
                return render(request, 'registro.html', {'error': 'El usuario ya existe!',
                                           'form': ()}
                )
    else:
        return render(request, 'registro.html', {'titulo':'Registro','message': 'Ingresa tus datos!',
                                           'form': RegistroForm()}
    )


@login_required
def signout(request):
    logout(request)
    return redirect('Home Page')

@login_required
def dashboard(request):
    tickets = Ticket.objects.all()
    return render(request, 'dashboard.html', {'tickets': tickets, 'title': 'Dashboard', 'message': 'Bienvenido al Dashboard'})
