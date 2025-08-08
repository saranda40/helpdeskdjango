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
from tickets import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='Home Page'),
    path('usuario/login/', views.ingreso, name='Login Page'),
    path('usuario/registro/', views.registro, name='Registro Page'),
    path('usuario/logout/', views.signout, name='Logout Page'),
    path('usuario/<int:id_usuario>/', views.profile, name='Profile Page'),
    path('dashboard/', views.dashboard, name='Dashboard Page'),
    path('tareas_completadas/', views.tareas_completadas, name='Tasks Completed Page'),
    path('tareas/tareas', views.tareas, name='Tareas Page'),
    path('tareas/crear', views.crear_tarea, name='Crear Tarea'),
    path('tareas/<int:id>/', views.detalle_tarea, name='Detalle Tarea Page'),
    path('tareas/<int:id>/complete/', views.completar_tarea, name='Tarea Completa Page'),
    path('tareas/<int:id>/delete/', views.eliminar_tarea, name='Tarea Eliminada Page'),
    # Add other URL patterns as needed
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
