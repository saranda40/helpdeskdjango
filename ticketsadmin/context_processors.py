# app2/context_processors.py

from .models import Empresa

def datos_empresa(request):
    try:
        # Aquí obtienes el primer objeto de configuración, asumiendo que solo hay uno
        config = Empresa.objects.first()
        return {
            'nombre_empresa': config.nombre_empresa,
            'logo_empresa': config.logo,
            # Otros valores que necesites
        }
    except Empresa.DoesNotExist:
        return {
            'nombre_empresa': 'Sebasti@n Dev',
        }