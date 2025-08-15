from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from tickets.models import cargos,areas

# Create your models here.

class Usuario(AbstractUser):
    apodo = models.TextField(max_length=20,null=True,blank=True)
    image_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    id_area = models.ForeignKey(areas, on_delete=models.CASCADE,null=True, blank=True)
    id_cargo = models.ForeignKey(cargos, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True)

    @property
    def es_supervisor(self):
        return bool(self.id_cargo and self.id_cargo.es_supervisor)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['username']
