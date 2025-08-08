from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import IntegrityError
from .models import Ticket
from ticketsadmin.models import Empresa, Anuncios
from usuarios.forms import LoginForm, RegistroForm, EditFormUser
from usuarios.models import Usuario
from .forms import Ticket
from django.utils import timezone  


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
                        password=request.POST['password1'],
                        first_name=request.POST['first_name'],
                        last_name=request.POST['last_name'],
                        email=request.POST['last_name'],
                        image_perfil=request.POST['image_perfil'],
                    )
                    print(request)
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

    if str(perfil.username) != str(request.user.username): # Corregido: comparar los atributos username
        return HttpResponse('No tienes permiso para editar este perfil.')
    
    if request.method == 'GET':
        form = EditFormUser(instance=perfil)
        return render(request, 'usuario/edita_usuario.html', {
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

@login_required
def dashboard(request):
    tickets = Ticket.objects.all()
    return render(request, 'dashboard.html', {'tickets': tickets, 'title': 'Dashboard', 'message': 'Bienvenido al Dashboard'})


############# TAREAS
@login_required
def tareas(request):
     if not request.user.is_authenticated:
        return render(request, 'login.html', {'titulo':'Login','message': 'Por favor, inicia sesión para ver tus tareas.', 'form': LoginForm()})
     tareas = Ticket.objects.filter(user=request.user,fecha_cierre_isnull=False).order_by('-fecha_cierre')
     if not tareas:
        return render(request, 'tareas/tareas.html', {'message': 'No tienes tareas pendientes.', 'tasks': tareas})
     else:
        return render(request, 'tareas/tareas.html', {'tasks': tareas,'titulo':'Listado', 'message': 'Tareas Page'})   

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
        form = Ticket(request.POST)
        if form.is_valid():
            if not request.user.is_authenticated:
                return render(request, 'login.html', {'message': 'Por favor, inicia sesión para crear una tarea.',
                                               'form': LoginForm()})
            # Save the task with the current user
      
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return render(request, 'tareas/crear_tareas.html', {'message': 'Tarea creada exitosamente!', 'form': LoginForm()})
        else:
            return render(request, 'tareas/crear_tareas.html', {'error': 'Error al crear la tarea!', 'form': form})
 else:
        if request.user.is_authenticated:
            return render(request, 'tareas/crear_tareas.html', {'message':'Nueva Tarea','error': 'Crear Tarea', 'form': LoginForm()})
        else:
            return render(request, 'login.html', {'message': 'Ingresa tus datos!',
                                              'form': LoginForm()})

@login_required    
def detalle_tarea(request, id_tarea):
    if not request.user.is_authenticated:
        return render(request, 'signin.html', {'message': 'Por favor, inicia sesión para ver los detalles de la tarea.',
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
            return redirect('Tasks Page')
        else:
            return render(request, 'detalle_tarea.html', {'error': 'Error al actualizar la tarea!', 'form': form})
    else:
        try:
            task = get_object_or_404(Ticket,pk=id_tarea, user=request.user)
            form = Ticket(instance=task)
            if task.user != request.user:
                return HttpResponse('No tienes permiso para ver esta tarea.')
            return render(request, 'tasks_detail.html', {'task': task, 
                                                        'message': 'Detalles de la Tarea',
                                                        'form': form})
        except Ticket.DoesNotExist:
            return render(request, 'signin.html', {'message': 'Ingresa tus datos!',
                                                'form': LoginForm()}) 
        
@login_required
def completar_tarea(request, task_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return render(request, 'login.html', {'message': 'Por favor, inicia sesión para completar una tarea.',
                                               'form': LoginForm()})
        task = get_object_or_404(Ticket, pk=task_id, user=request.user)
      
        if task.user != request.user:
            return HttpResponse('No tienes permiso para completar esta tarea.')
        task.datecompleted = timezone.now()
        task.save()
        return redirect('Tasks Page') 

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
        return redirect('Tasks Page')