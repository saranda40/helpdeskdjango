from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from ..models import Ticket
from usuarios.forms import LoginForm
from usuarios.models import Usuario
from ..forms import  AsignarForm, BusquedaAsignacion
from django.utils import timezone
from icecream import ic
from django.core.paginator import Paginator

@login_required
def asignaciones(request):
      if not Usuario.es_supervisor:
          render(request, 'error.html', {'titulo':'Login','error': 'Su perfil no permite revisar asignaciones de Tickets, consulte con su Administrador.'})
      if not request.user.is_authenticated:
                return render(request, 'login.html', {'titulo':'Login','message': 'Por favor, inicia sesión para ver tus tareas.', 'form': LoginForm()})
      id_area_usuario = request.user.id_area.id
      asignaciones = Ticket.objects.filter(asignado_a__isnull=True, id_area = id_area_usuario).values('id','titulo','descripcion','id_area__nombre','id_nivel__nombre','fecha_creacion').order_by('-fecha_creacion')
      headers = ['Ticket','Título','Área','F. Creación']
      actions = [
        {
            'url_name': 'Detalle Asignacion Page',
            'title': 'Asignar Tarea',
            'class': 'btn-success',
            'icon_class': 'ti ti-file-check',
            'type': 'all', 
        },
        {
            'url_name': 'Tarea Eliminada Page',
            'title': 'Eliminar Tarea',
            'class': 'btn-danger',
            'icon_class': 'ti ti-trash',
            'type': 'all', 
        }
    ]
      if not asignaciones:
             return render(request,'tareas/asignaciones.html',{'titulo':'Asignaciones','message':'No tiene asignaciones de casos por revisar','headers':headers,
                                                               'asignaciones':asignaciones,'valor':'asignar'})
             
      else:
            data = [
                {
                    'id': usuario['id'],
                    'titulo': usuario['titulo'],
                    'area': usuario['id_area__nombre'],
                    'fecha': usuario['fecha_creacion'].strftime('%d-%m-%Y')
                } for usuario in asignaciones
            ]
            ic(data)
            form = BusquedaAsignacion
            paginator = Paginator(asignaciones, 10)  # Mostrar 10 usuarios por página
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request, 'tareas/asignaciones.html', {
                'titulo': 'Asignaciones',
                'message': 'Listado asignaciones por revisar',
                'headers': headers,
                'data': data,
                'page_obj': page_obj,
                'keys': ['id', 'titulo', 'area','fecha'],
                'actions': actions,
                'form': form
                })
            #return render(request,'tareas/asignaciones.html',{'titulo':'Asignaciones','message':'Listado asignaciones por revisar','headers':headers,'asignaciones':asignaciones,'valor':'asignar'})
             
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