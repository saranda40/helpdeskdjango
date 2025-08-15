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
def asignaciones(request):
      if not Usuario.es_supervisor:
          render(request, 'error.html', {'titulo':'Login','error': 'Su perfil no permite revisar asignaciones de Tickets, consulte con su Administrador.'})
      if not request.user.is_authenticated:
                return render(request, 'login.html', {'titulo':'Login','message': 'Por favor, inicia sesión para ver tus tareas.', 'form': LoginForm()})
      id_area_usuario = request.user.id_area.id
      asignaciones = Ticket.objects.filter(asignado_a__isnull=True, id_area = id_area_usuario).values('id','titulo','descripcion','id_area__nombre','id_nivel__nombre').order_by('-fecha_creacion')
      headers = ['id','Título','Descripción','Área','Nivel']
      if not asignaciones:
             return render(request,'tareas/asignaciones.html',{'titulo':'Asignaciones','message':'No tiene asignaciones de casos por revisar','headers':headers,
                                                               'asignaciones':asignaciones,'valor':'asignar'})
      else:
             return render(request,'tareas/asignaciones.html',{'titulo':'Asignaciones','message':'Listado asignaciones por revisar','headers':headers,'asignaciones':asignaciones,'valor':'asignar'})
             


@login_required
def asignaciones_detalle(request, id):
        return request
