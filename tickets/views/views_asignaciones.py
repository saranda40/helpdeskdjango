from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import IntegrityError
from ..models import Ticket
from ticketsadmin.models import Empresa, Anuncios
from usuarios.forms import LoginForm, RegistroForm, EditFormUser
from usuarios.models import Usuario, cargos
from ..forms import MensajesTicket,  RespuestaMensajeTicket, TicketForm, AsignarForm
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
      headers = ['Ticket','Título','Descripción','Área','Nivel']
      if not asignaciones:
             return render(request,'tareas/asignaciones.html',{'titulo':'Asignaciones','message':'No tiene asignaciones de casos por revisar','headers':headers,
                                                               'asignaciones':asignaciones,'valor':'asignar'})
      else:
             return render(request,'tareas/asignaciones.html',{'titulo':'Asignaciones','message':'Listado asignaciones por revisar','headers':headers,'asignaciones':asignaciones,'valor':'asignar'})
             
@login_required
def asignaciones_detalle(request, id):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'titulo':'Login','message': 'Por favor, inicia sesión para ver los detalles de la asignación.', 'form': LoginForm()})
    
    if request.method == 'POST':
        try:
            form = AsignarForm(request.POST)
            if form.is_valid():
                 ticket = get_object_or_404(Ticket,pk=id, user =request.user)
                 ic(ticket)
                 ticket.id_nivel = form.cleaned_data['id_nivel']
                 ticket.asignado_a = form.cleaned_data['asignado_a']
                 ticket.fecha_asignacion = timezone.now()

                 ticket.save()
                 return redirect('Asignaciones Page')
        except IntegrityError:
            return render(request, 'error.html', {'titulo':'Error','error': 'No se pudo asignar el ticket. Intente nuevamente.'})
    else:
        try:
            ticket = get_object_or_404(Ticket, id=id, user=request.user)
            if ticket.asignado_a is not None:
                return render(request, 'error.html', {'titulo':'Error','error': 'El ticket ya ha sido asignado.'})
            form = AsignarForm(instance=ticket, user =request.user)
            return render(request, 'tareas/detalle_asignaciones.html', {'titulo':'Detalle Asignación Ticket: '+ str(ticket.id),'ticket':ticket,'form': form})
        except Ticket.DoesNotExist:
            return render(request, 'error.html', {'titulo':'Error','error': 'Ticket no encontrado.'})

@login_required
def completa_asignaciones_detalle(request, id):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'titulo':'Login','message': 'Por favor, inicia sesión para completar la asignación.', 'form': LoginForm()})
    ticket = get_object_or_404(Ticket, id=id)
    if ticket.asignado_a is None:
        return render(request, 'error.html', {'titulo':'Error','error': 'El ticket no ha sido asignado.'})
    if request.method == 'POST':
        try:
            ticket.asignado_a = ticket.cleaned_data['asigando_a']
            ticket.id_nivel = ticket.cleaned_data['id_nivel']
            ticket.fecha_asignacion = timezone.now()

            ticket.save()
            return redirect('Asignaciones Page')
        except IntegrityError:
            return render(request, 'error.html', {'titulo':'Error','error': 'No se pudo completar la asignación. Intente nuevamente.'})
    else:
        return render(request, 'tareas/detalle_asignaciones.html', {'titulo':'Completar Asignación Ticket: '+ str(ticket.id),'ticket':ticket})