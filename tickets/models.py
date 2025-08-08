from django.db import models
from django.conf import settings

# Create your models here.

class Ticket(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    id_nivel = models.ForeignKey('nivel', on_delete=models.CASCADE, null=True, blank=True)
    id_area = models.ForeignKey('areas', on_delete=models.CASCADE, null=True, blank=True)
    id_cargo = models.ForeignKey('cargos', on_delete=models.CASCADE, null=True, blank=True)
    asignado_a = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assigned_tickets', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - ' + str(self.user.username)
    
    class Meta:
        ordering = ['-fecha_creacion']  # Ordenar por fecha de creación descendente
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

class imagenes(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    imagen = models.ImageField(upload_to='imagenes/')
    id_ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.imagen.name + ' - ' + str(self.id_ticket.id) if self.id_ticket else self.imagen.name
    class Meta:
        verbose_name = 'Imagen'
        verbose_name_plural = 'Imágenes'
    
# Alto,bajo,medio
class nivel(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    is_activo = models.BooleanField(default=True)
    prioridad = models.IntegerField(default=0) 

    def __str__(self):
        return self.nombre + ' - ' + str(self.prioridad)

    class Meta:
        verbose_name = 'Nivel'
        verbose_name_plural = 'Niveles'
        ordering = ['id']

class areas(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    is_activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'

class cargos(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()    
    es_supervisor = models.BooleanField(default=False)
    id_area = models.ForeignKey('areas', on_delete=models.CASCADE, null=True, blank=True)
    is_activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['id']
