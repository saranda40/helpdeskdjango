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

@login_required
def crear_mensaje(request, id_ticket):
    numero_ticket = Usuario.objects.filter(id==id_ticket)

    ic(numero_ticket)
    if not request.user.is_authenticated:
                return render(request, 'signin.html', {'message': 'Por favor, inicia sesión para crear un Mensaje.',
                                               'form': LoginForm()})
          
    if request.method  == 'POST':
        form  = MensajesTicket(request.POST)
        if form.is_valid():
            Mensaje = form.save(commit = False)
            Mensaje.user = request.user
            Mensaje.save()
            return render('tareas/crear_tarea.html',{'titulo':'Crear Mensaje','message':'Mensaje creado exitosamente para Ticket:' + numero_ticket ,'form':MensajesTicket})

    else:
        form = MensajesTicket()
    return render(request,'mensajes/crear_mensaje.html',{'titulo':'Crear Mensaje','message':'Crear nuevo Mensaje para Ticket:' + numero_ticket ,'form':form})
