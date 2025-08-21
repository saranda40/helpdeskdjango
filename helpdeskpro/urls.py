
from django.contrib import admin
from django.urls import path
from tickets.views import views_asignaciones, views_mensajes, views_sitio, views_tareas, views_usuarios, views_admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('administrador/usuarios',views_admin.listar_usuarios, name='Usuarios Page'),
    path('administrador/usuarios/<int:id_usuario>/', views_admin.editar_usuario, name='Editar Usuario Page'),
    path('administrador/usuarios/eliminar/<int:id_usuario>/', views_admin.eliminar_usuario, name='Eliminar Usuario Page'),
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
