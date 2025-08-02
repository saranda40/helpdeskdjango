from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Usuario(AbstractUser):
    image_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['username']