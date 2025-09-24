from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import IntegrityError
from ..models import Ticket
from ticketsadmin.models import Empresa, Anuncios
from usuarios.forms import LoginForm, RegistroForm, EditFormUser
from usuarios.models import Usuario, cargos
from ..forms import MensajesTicket,  RespuestaMensajeTicket, TicketForm, RevisaTicketForm
from django.utils import timezone
from icecream import ic
from django.http import JsonResponse

@login_required
def asignar_tarea(request):
    ic(request)

@login_required
def tareas(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'titulo':'Login','message': 'Por favor, inicia sesión para ver tus tareas.', 'form': LoginForm()})
    tareas = Ticket.objects.filter(asignado_a=request.user.id,fecha_cierre__isnull=True).values('id','titulo','descripcion','id_nivel__nombre','id_area__nombre').order_by('-fecha_cierre')
    headers = ['id','Título','Descripción', 'Nivel', 'Área']

    if tareas:
        return render(request, 'tareas/tareas.html', {'titulo':'Tickets','message': 'Tickets pendientes.','headers':headers, 'tasks': tareas,'valor':'revisar'})
    else:
        return render(request, 'tareas/tareas.html', {'tasks': tareas,'titulo':'Listado', 'message': 'Tareas Page'})   

@login_required
def revision_tarea(request, id):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'titulo':'Login','message': 'Por favor, inicia sesión para ver los detalles de la tarea.', 'form': LoginForm()})
    
    try:
        ticket = get_object_or_404(Ticket, pk=id, asignado_a=request.user.id)
        form = RevisaTicketForm(instance=ticket)
        return render(request, 'tareas/revision_tarea.html', {'titulo':'Revisión Ticket: '+ str(ticket.id),'ticket':ticket,'form': form})
    except Ticket.DoesNotExist:
        return render(request, 'error.html', {'titulo':'Error','error': 'Ticket no encontrado.'})

@login_required
def tareas_completadas(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'message': 'Por favor, inicia sesión para ver tus tareas.', 'form': LoginForm()})
    tasks = Ticket.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    if not tasks:
        return render(request, 'tareas.html', {'message': 'No tienes tareas pendientes.', 'tasks': tasks})
    else:
        return render(request, 'tareas.html', {'tasks': tasks, 'message': 'Tareas Page'})    
 
 
@login_required
def crear_tarea(request):
 if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            if not request.user.is_authenticated:
                return render(request, 'login.html', {'message': 'Por favor, inicia sesión para crear una tarea.',
                                               'form': LoginForm()})
            # Save the task with the current user
            ic(form)
            task = form.save(commit=False)
            task.id_area = 2
            task.user = request.user
            task.save()
            return render(request, 'tareas/crear_tarea.html', {'message': 'Tarea creada exitosamente!', 'form': form})
        else:
            return render(request, 'tareas/crear_tarea.html', {'error': 'Error al crear la tarea!', 'form': form})
 else:
        if request.user.is_authenticated:
            return render(request, 'tareas/crear_tarea.html', {'titulo':'Nueva Tarea','message':'Crear nueva Tarea', 'form': TicketForm()})
        else:
            return render(request, 'login.html', {'message': 'Ingresa tus datos!',
                                              'form': LoginForm()})

@login_required    
def detalle_tarea(request, id_tarea):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'message': 'Por favor, inicia sesión para ver los detalles de la tarea.',
                                               'form': LoginForm()})
    if request.method == 'POST':
        form = Ticket(request.POST)
        if form.is_valid():
            task = get_object_or_404(Ticket, pk=id_tarea, user=request.user)
            if task.user != request.user:
                return HttpResponse('No tienes permiso para editar esta tarea.')
            task.title = form.cleaned_data['title']
            task.description = form.cleaned_data['description']
            task.important = form.cleaned_data['important']
            task.save()
            return redirect('Tareas Page')
        else:
            return render(request, 'tareas/detalle_tarea.html', {'error': 'Error al actualizar la tarea!', 'form': form})
    else:
        try:
            task = get_object_or_404(Ticket,pk=id_tarea, user=request.user)
            form = Ticket(instance=task)
            if task.user != request.user:
                return HttpResponse('No tienes permiso para ver esta tarea.')
            return render(request, 'tareas/detalle_tarea.html', {'task': task, 
                                                        'message': 'Detalles de la Tarea',
                                                        'form': form})
        except Ticket.DoesNotExist:
            return render(request, 'usuarios/registro.html', {'message': 'Ingresa tus datos!',
                                                'form': LoginForm()}) 
        
@login_required
def completar_tarea(request, id):
    ic(id)
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'titulo':'Login','message': 'Por favor, inicia sesión para completar una tarea.', 'form': LoginForm()})
    if request.method == 'POST':
        task = get_object_or_404(Ticket, pk=id)
      
        if task.asignado_a != request.user:
            return render(request, 'error.html', {'titulo':'Error','error': 'No tienes permiso para completar esta tarea.'})
        task.fecha_cierre = timezone.now()
        task.is_cerrado = True
        task.save()
        return redirect('Tareas Page') 

@login_required
def eliminar_tarea(request, task_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return render(request, 'signin.html', {'message': 'Por favor, inicia sesión para eliminar una tarea.',
                                               'form': LoginForm()})
        task = get_object_or_404(Ticket, pk=task_id, user=request.user)
        if task.user != request.user:
            return HttpResponse('No tienes permiso para eliminar esta tarea.')
        task.delete()
        return redirect('Tareas Page')

