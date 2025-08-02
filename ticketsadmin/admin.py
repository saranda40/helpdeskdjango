from django.contrib import admin
from .models import Empresa, Anuncios, TipoAnuncio
# Register your models here.

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre_empresa', 'descripcion_empresa')
    search_fields = ('nombre_empresa',) 
    readonly_fields = ('id',)   

class AnunciosAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'contenido', 'fecha_creacion', 'fecha_publicacion', 'fecha_termino', 'is_activo')
    search_fields = ('titulo', 'contenido')

class TipoAnuncioAdmin(admin.ModelAdmin):
    list_display = ('nombre','descripcion')
    search_fields = ('nombre','descripcion')
    readonly_fields = ('idTipoAnuncio',)   

admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Anuncios, AnunciosAdmin)
admin.site.register(TipoAnuncio,TipoAnuncioAdmin)
# Register your models h    ere.
