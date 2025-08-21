from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from usuarios.forms import LoginForm, EditFormUser, BuscarUsuarioForm
from usuarios.models import Usuario

from icecream import ic


    
@login_required
def editar_usuario(request, id_usuario):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'message': 'Regístrese', 'form': LoginForm()})
    
    usuario = get_object_or_404(Usuario, pk=id_usuario)

    if str(usuario.username) != str(request.user.username) and not request.user.is_administrador: 
        return HttpResponse('No tienes permiso para editar este usuario.')
    
    if request.method == 'GET':
        form = EditFormUser(instance=usuario)
        return render(request, 'usuarios/edita_usuario.html', {
            'Usuario': usuario,
            'form': form,
            'titulo': 'Editar Usuario',
            'message': 'Datos de usuario: ' + usuario.username
        })
    else:  # request.method == 'POST'
        form = EditFormUser(request.POST, request.FILES, instance=usuario)
        
        if form.is_valid():
            form.save()
            return redirect('Usuarios Page')
        else:
            return render(request, 'usuarios/edita_usuario.html', {
                'Usuario': usuario,
                'form': form,
                'titulo': 'Editar Usuario',
                'message': 'Error al actualizar información'
            })

@login_required
def eliminar_usuario(request, id_usuario):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'message': 'Regístrese', 'form': LoginForm()})
    
    usuario = get_object_or_404(Usuario, pk=id_usuario)

    if str(usuario.username) != str(request.user.username) and not request.user.is_administrador: 
        return HttpResponse('No tienes permiso para eliminar este usuario.')
    
    if request.method == 'POST':
        usuario.is_active = False
        usuario.save()
        return redirect('Usuarios Page')
    else:
        return render(request, 'usuarios/eliminar_usuario.html', {
            'Usuario': usuario,
            'titulo': 'Eliminar Usuario',
            'message': '¿Estás seguro de que quieres eliminar este usuario?'
        })

@login_required
def listar_usuarios(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'message': 'Regístrese', 'form': LoginForm()})
    
    if not request.user.is_administrador:
        return render(request, 'error.html', {'message': 'No tienes permiso para acceder a esta página.'})

    
    form = BuscarUsuarioForm(request.GET or None)
    ic(form)

    headers = ['ID', 'Usuario', 'Nombre Completo', 'Apodo' ,'Área', 'Cargo', 'Activo']
    actions = [
        {
            'url_name': 'Editar Usuario Page',
            'title': 'Editar Usuario',
            'class': 'btn-success',
            'icon_class': 'ti ti-file-check',
        },
        {
            'url_name': 'Eliminar Usuario Page',
            'title': 'Eliminar Usuario',
            'class': 'btn-danger',
            'icon_class': 'ti ti-trash',
        },
    ]
    
    if form.is_valid():
        busqueda_texto = form.cleaned_data.get('username')
        area = form.cleaned_data.get('id_area')


        if busqueda_texto:
            lista_Usuarios = Usuario.objects.filter(Q(first_name__icontains=busqueda_texto) | Q(last_name__icontains=busqueda_texto) | Q(username__icontains=busqueda_texto) | Q(apodo__icontains=busqueda_texto), is_active=True, is_superuser=False)

        if area:
            lista_Usuarios = lista_Usuarios.filter(id_area=area)

        
        if not busqueda_texto and not area:
            lista_Usuarios = Usuario.objects.filter(is_active=True, is_superuser=False).order_by('username')
        


        paginator = Paginator(lista_Usuarios, 10)  # Mostrar 10 usuarios por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        data = [
            {
                'id': usuario.id,
                'username': usuario.username,
                'nombre_completo': usuario.get_full_name(),
                'apodo': usuario.apodo,
                'area': usuario.id_area.nombre if usuario.id_area else 'N/A',
                'cargo': usuario.id_cargo.nombre if usuario.id_cargo else 'N/A',
                'activo': 'Sí' if usuario.is_active else 'No'
            } for usuario in lista_Usuarios
        ]
        
        return render(request, 'usuarios/usuarios.html', {
            'titulo': 'Lista de Usuarios',
            'message': 'Usuarios activos en el sistema',
            'headers': headers,
            'data': data,
            'page_obj': page_obj,
            'keys': ['id', 'username', 'nombre_completo', 'apodo', 'area', 'cargo', 'activo'],
            'actions': actions,
            'form': form
        })
    
    else:
        form = BuscarUsuarioForm()
        lista_Usuarios = Usuario.objects.filter(is_active=True, is_superuser=False).order_by('username')
        paginator = Paginator(lista_Usuarios, 10)  # Mostrar 10 usuarios por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        data = [
            {
                'id': usuario.id,
                'username': usuario.username,
                'nombre_completo': usuario.get_full_name(),
                'apodo': usuario.apodo,
                'area': usuario.id_area.nombre if usuario.id_area else 'N/A',
                'cargo': usuario.id_cargo.nombre if usuario.id_cargo else 'N/A',
                'activo': 'Sí' if usuario.is_active else 'No'
            } for usuario in lista_Usuarios
        ]

        return render(request, 'usuarios/usuarios.html', {
            'titulo': 'Lista de Usuarios',
            'message': 'Usuarios activos en el sistema',
            'headers': headers,
            'data': data,
            'page_obj': page_obj,
            'keys': ['id', 'username', 'nombre_completo', 'apodo', 'area', 'cargo', 'activo'],
            'actions': actions,
            'form': form
        })





    

    
@login_required
def usuarios_list(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'message': 'Regístrese', 'form': LoginForm()})
    
    if not request.user.is_administrador:
        return HttpResponse('No tienes permiso para acceder a esta página.')
    
    usuarios = Usuario.objects.filter(is_active=True,is_superuser=False ).order_by('username')
    headers = ['ID', 'Usuario', 'Nombre Completo', 'Apodo' ,'Área', 'Cargo', 'Activo']
    actions = [
        {
            'url_name': 'Editar Usuario Page',
            'title': 'Editar Usuario',
            'class': 'btn-success',
            'icon_class': 'ti ti-file-check',
        },
        {
            'url_name': 'Eliminar Usuario Page',
            'title': 'Eliminar Usuario',
            'class': 'btn-danger',
            'icon_class': 'ti ti-trash',
        },
    ]

    data = [
        {
            'id': usuario.id,
            'username': usuario.username,
            'nombre_completo': usuario.get_full_name(),
            'apodo': usuario.apodo,
            'area': usuario.id_area.nombre if usuario.id_area else 'N/A',
            'cargo': usuario.id_cargo.nombre if usuario.id_cargo else 'N/A',
            'activo': 'Sí' if usuario.is_active else 'No'
        } for usuario in usuarios
    ]
    
    return render(request, 'usuarios/usuarios.html', {
        'titulo': 'Lista de Usuarios',
        'message': 'Usuarios activos en el sistema',
        'headers': headers,
        'data': data,
        'keys': ['id', 'username', 'nombre_completo', 'apodo', 'area', 'cargo', 'activo'],
        'actions': actions
    })