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
# Create your views here.

def home(request):
    holding = Empresa.objects.first()
    if not holding:
        return HttpResponse("No hay información de la empresa disponible.")
    informaciones = Anuncios.objects.filter(is_activo=True)
    return render(request, 'home.html', {'title': 'Tickets', 'message': 'Sistema de Ingreso de Tickets',
                                                   'empresa': holding.nombre_empresa,
                                                   'anuncios': informaciones})


@login_required
def dashboard(request):
    if request.user.es_supervisor:
        supervisor = True
    else:
        supervisor = False
    
    apodo = request.user.apodo
    cargo=request.user.id_cargo
    ahora = timezone.now().year

    tickets = Ticket.objects.all()
    return render(request, 'dashboard.html', {'tickets': tickets, 
                                              'title': 'Dashboard', 
                                              'message': 'Bienvenido al Dashboard',
                                              'supervisor': supervisor,
                                              'apodo': apodo,
                                              'cargo':cargo,
                                              'year':ahora})


###### vistas AJAX
def get_cargos_por_area(request):
    id_area = request.GET.get('id_area')
    try:
        info_cargos = cargos.objects.filter(
            id_area__id=id_area,
            is_activo=True
        )
        data = [{'id': cargo.id, 'cargo': cargo.nombre} for cargo in info_cargos]
        ic(data)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def get_usuarios_por_area(request):
    id_area = request.GET.get('id_area')
    current_user_id = request.user.id
    
    try:
        usuarios = Usuario.objects.filter(
            id_area__id=id_area,
            is_superuser=False,
            is_active=True
        ).exclude(id=current_user_id).order_by('username')
        
        data = [{'id': usuario.id, 'username': usuario.username} for usuario in usuarios]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)