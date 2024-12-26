#Esta app se trabaja con el ORM de Django para el manejo seguro con la base de datos
#se dejará la documentacion segun sus base de datos MYSQL - POSTGRES - SQLITE3
from django.shortcuts import render

#manejar paginación de tablas a 10 campos, rendimiento.
from django.core.paginator import Paginator


#manejar hora actual
from datetime import datetime

#usaremos LOS DATOS de los condominios
from condominio.models import PerfilUsuario, RegistroVisita, RegistroAutomovil, RegistroMascota, RegistroReporte


#APLICACION DE OFICIALES 
    #LOS OFICIALES VEN TODOS LOS DATOS DE LOS CONDÓMINOS



#mis herramientas
class MisHerramientas:
    def __init__(self):
        self.hora_actual = self.obtener_hora()
    
    def obtener_hora(self):
        hora_local = datetime.now()
        
        #format_24 = hora_local.strftime(" %Y - %m - %d,- %H: %M: %S")
        format_12 = hora_local.strftime(" %Y - %m - %d,- %I: %M: %S %p")
        return str(format_12)
        

#funcion para mostrar todos los datos de los condominios
def todo (request,**kwargs):
    
    #guardameros todos los registros en variables
    permanentes = PerfilUsuario.objects.all().order_by("usuario")
    #creo una instancia y digo que solo 10 voy a mostrar en el html
    paginador = Paginator(permanentes, 10)
    #obtengo el numero de pagina de la paginacion condominio/2
    pagina_numero = request.GET.get("page")
    
    
    
    #pagina correspondiente con valores fuera de rango
    pagina_objeto_permanentes = paginador.get_page(pagina_numero)
    
    #crearemos paginacion para todos los datos Aplicacion proyecto general
    
    mascotas = RegistroMascota.objects.all().order_by("fecha_creado")
    #guardameros todos los registros en variables
    #creo una instancia y digo que solo 10 voy a mostrar en el html
    paginador = Paginator(mascotas, 10)
    #obtengo el numero de pagina de la paginacion condominio/2
    pagina_numero = request.GET.get("page")
    #pagina correspondiente con valores fuera de rango
    pagina_objeto_mascotas = paginador.get_page(pagina_numero)
    
    

    reportes = RegistroReporte.objects.all().order_by("fecha_creado")
    #guardameros todos los registros en variables
    #creo una instancia y digo que solo 10 voy a mostrar en el html
    paginador = Paginator(reportes, 10)
    #obtengo el numero de pagina de la paginacion condominio/2
    pagina_numero = request.GET.get("page")
    #pagina correspondiente con valores fuera de rango
    pagina_objeto_reportes = paginador.get_page(pagina_numero)
    
    
    
    automoviles =RegistroAutomovil.objects.all().order_by("usuario") #.select_related("usuario")
    #guardameros todos los registros en variables
    #creo una instancia y digo que solo 10 voy a mostrar en el html
    paginador = Paginator(automoviles, 10)
    #obtengo el numero de pagina de la paginacion condominio/2
    pagina_numero = request.GET.get("page")
    #pagina correspondiente con valores fuera de rango
    pagina_objeto_automoviles = paginador.get_page(pagina_numero)
    
    
    visitas_diarias_todas = RegistroVisita.objects.all().order_by("usuario") #.select_related("usuario")  #.select_related("usuario") para relacionar 
    #guardameros todos los registros en variables
    #creo una instancia y digo que solo 10 voy a mostrar en el html
    paginador = Paginator(visitas_diarias_todas, 10)
    #obtengo el numero de pagina de la paginacion condominio/2
    pagina_numero = request.GET.get("page")
    #pagina correspondiente con valores fuera de rango
    pagina_objeto_visitas_diarias_todas = paginador.get_page(pagina_numero)
        
    
    #contatenamos
    hora_actual = MisHerramientas().hora_actual
    
    
    return render(request, 'oficiales/todo.html', {"pagina_objeto_permanentes":pagina_objeto_permanentes,"pagina_objeto_visitas_diarias_todas":pagina_objeto_visitas_diarias_todas, "pagina_objeto_automoviles":pagina_objeto_automoviles,"pagina_objeto_mascotas": pagina_objeto_mascotas,"pagina_objeto_reportes":pagina_objeto_reportes, "hora_actual": hora_actual})



#FALTA CLEAN CODE
def visitas_Autorizadas (request):
    pass

def permanentes (request):
    pass

def mascotas_condominio (request):
    pass

def auto_condominio (request):
    pass