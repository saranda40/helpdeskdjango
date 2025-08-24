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
    is_admin = models.BooleanField(default=False, null=True)
    crea_ticket = models.BooleanField(default=False, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    @property
    def es_supervisor(self):
        return bool(self.id_cargo and self.id_cargo.es_supervisor)

    @property
    def is_administrador(self):
        return bool(self.is_admin)

    def __str__(self):
        return f"{self.username} ({self.apodo})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name} ({self.apodo})"
    
    def get_short_name(self):
        return self.first_name
    
    @property
    def nombre_completo(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def nombre_usuario(self):
        return self.apodo if self.apodo else self.username

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['username']

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['username']
