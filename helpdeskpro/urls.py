"""
URL configuration for helpdeskpro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tickets.views import views_asignaciones, views_mensajes, views_sitio, views_tareas, views_usuarios
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views_sitio.home, name='Home Page'),
    path('usuario/login/', views_usuarios.ingreso, name='Login Page'),
    path('usuario/registro/', views_usuarios.registro, name='Registro Page'),
    path('usuario/logout/', views_usuarios.signout, name='Logout Page'),
    path('usuario/<int:id_usuario>/', views_usuarios.profile, name='Profile Page'),
    path('dashboard/', views_sitio.dashboard, name='Dashboard Page'),
    path('tareas_completadas/', views_tareas.tareas_completadas, name='Tasks Completed Page'),
    path('tareas/tareas', views_tareas.tareas, name='Tareas Page'),
    path('tareas/asignar', views_tareas.asignar_tarea, name='Asignar Tareas Page'),
    path('tareas/crear_tarea', views_tareas.crear_tarea, name='Crear Tarea Page'),
    path('tareas/<int:id>/', views_tareas.detalle_tarea, name='Detalle Tarea Page'),
    path('tareas/<int:id>/revision/', views_tareas.revision_tarea, name='Revisión Ticket Page'),
    path('tareas/<int:id>/complete/', views_tareas.completar_tarea, name='Tarea Completa Page'),
    path('tareas/<int:id>/delete/', views_tareas.eliminar_tarea, name='Tarea Eliminada Page'),
    path('tareas/asignaciones',views_asignaciones.asignaciones, name='Asignaciones Page'),
    path('tareas/asignaciones/<int:id>',views_asignaciones.asignaciones_detalle, name='Detalle Asignacion Page'),
    path('get_cargos_por_area', views_sitio.get_cargos_por_area, name='get_cargos_por_area'),
    # Add other URL patterns as needed
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
