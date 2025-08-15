from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import IntegrityError
from ..models import Ticket
from ticketsadmin.models import Empresa, Anuncios
from usuarios.forms import LoginForm, RegistroForm, EditFormUser
from usuarios.models import Usuario, cargos
from ..forms import MensajesTicket,  RespuestaMensajeTicket, TicketForm
from django.utils import timezone
from icecream import ic
from django.http import JsonResponse


def ingreso(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('Dashboard Page')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos!','form': LoginForm()})
    else:
        return render(request, 'login.html', {'titulo': 'login',
                                              'message': 'Ingresa tus credenciales!',
                                              'form': LoginForm})

def registro(request):
    if request.method == 'POST':
        if request.POST['username'] and request.POST['password1'] and request.POST['password2'] and request.POST['email'] and request.POST['first_name'] and request.POST['last_name'] and request.POST['password2']:
            try:
                if request.POST['password1'] == request.POST['password2']:
                    ic(request.POST['image_perfil'])
                    user = Usuario.objects.create_user(
                    apodo=request.POST['apodo'],
                    username=request.POST['username'],
                    password=request.POST['password1'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    email=request.POST['email'],
                    image_perfil=request.POST['image_perfil'],
                    )
                    ic(request)
                    user.save()
                    login(request, user)
                    return redirect('Dashboard Page')
                else:
                    return render(request, 'usuarios/registro.html', {'error': 'Contraseñas no coinciden!',
                                           'form': RegistroForm()}
                )
            except IntegrityError:
                return render(request, 'usuarios/registro.html', {'error': 'El usuario ya existe!',
                                           'form': ()}
                )
    else:
        return render(request, 'usuarios/registro.html', {'titulo':'Registro','message': 'Ingresa tus datos!',
                                           'form': RegistroForm()}
    )

@login_required
def profile(request, id_usuario):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'message': 'Regístrese', 'form': LoginForm()})

    perfil = get_object_or_404(Usuario, pk=id_usuario)

    if str(perfil.username) != str(request.user.username): 
        return HttpResponse('No tienes permiso para editar este Perfil.')
    
    if request.method == 'GET':
        form = EditFormUser(instance=perfil)
        return render(request, 'usuarios/edita_usuario.html', {
            'Usuario': perfil,
            'form': form,
            'titulo': 'Editar Usuario',
            'message': 'Datos de usuario: ' + perfil.username
        })
    else:  # request.method == 'POST'
        form = EditFormUser(request.POST, request.FILES, instance=perfil) # Corregido: pasar la instancia y request.FILES
        
        if form.is_valid():
            form.save() # Corregido: usar form.save() para actualizar el objeto
            return redirect('Dashboard Page')
        else:
            return render(request, 'usuario/edita_usuario.html', {
                'Usuario': perfil,
                'form': form, # Corregido: pasar el formulario con errores
                'titulo': 'Editar Usuario',
                'message': 'Error al actualizar información'
            })
        
@login_required
def signout(request):
    logout(request)
    return redirect('Home Page')
