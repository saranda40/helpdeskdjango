from django.contrib import admin
from .models import Ticket, imagenes, nivel, areas, cargos

class TicketAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha_creacion', 'fecha_cierre')
    list_display = ('titulo', 'user', 'fecha_creacion', 'fecha_cierre', 'asignado_a')
    search_fields = ('titulo', 'user__username')

class ImagenesAdmin(admin.ModelAdmin):
    list_display = ('imagen', 'id_ticket')
    search_fields = ('id_ticket__titulo',)

class NivelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

class AreasAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')    

class CargosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'es_supervisor', 'id_area')
    search_fields = ('nombre', 'id_area__nombre')

admin.site.register(Ticket, TicketAdmin)
admin.site.register(imagenes, ImagenesAdmin)
admin.site.register(nivel, NivelAdmin)
admin.site.register(areas, AreasAdmin)
admin.site.register(cargos, CargosAdmin)
# Register your models here.
