from django.contrib import admin
from .models import PerfilUsuario, RegistroAutomovil,RegistroMascota,RegistroReporte,RegistroVisita
# Register your models here.


#forma basica de registrar las tablas de esta app em el admin DJANGO 
admin.site.register(RegistroAutomovil)
admin.site.register(RegistroMascota)
admin.site.register(RegistroReporte)


#segunda forma
@admin.register(PerfilUsuario)
class RegistroVisitaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "casa",)
    search_fields = ("usuario_username","casa")
    
#segunda forma

@admin.register(RegistroVisita)
class RegistroVisitaAdmin(admin.ModelAdmin):
    # Configuraciones adicionales del admin si lo deseas
    pass