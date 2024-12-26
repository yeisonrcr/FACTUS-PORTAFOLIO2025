from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#creamos las tablas y las relaciones 


#Tabla PerfilUsuario
class PerfilUsuario(models.Model):
    #relacion entre esta tabla y la tabla usuario esto 
    #para majenar por usuario /En el proyecto usaremos el usuario general
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    casa = models.CharField(max_length=100, null=True, blank=True)
    integrantes_permanente = models.CharField(max_length=1000)
    placas_permanentes = models.CharField(max_length=1000)
    fecha_creado = models.DateTimeField(default=timezone.now)

    #mostrar datos en el admin
    def __str__(self):
        return f" Casa {self.casa} : Integrantes Permanentes {self.integrantes_permanente} : {self.placas_permanentes} "


    #manejamos el guardado de alguna mascota por alguna seguridad aparte etc
    def save (self, *args , **kwargs):
        
        #valdacion personalizada para guardar la visita
        self.casa = self.usuario.username  #ID o USERNAME USUARIO LOGEADO EN EL SISTEMA
            #Este es el proyecto del portafolio por ende, tendra todas las aplicaciones con un solo usuario
            #Aca guardariamos la casa del usuario a la hora de crear el user_condominio, username, password, casa, nombre, placa en el app 1
            
        super().save(*args, **kwargs)
    
    class meta:#legible para el usuario en admin
        
        indexes = [
            "personas_autorizadas", "placas_autorizadas"
        ]
        
        #nombre que toman en el admin
        verbose_name="Visita"
        verbose_name_plural="Visitas"

# Tabla RegistroVisitas
class RegistroVisita(models.Model):
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) #relacion
    personas_visitantes = models.CharField(max_length=1000, null=False)
    placas_autorizadas = models.CharField(max_length=500, null=True , blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return f" Autorizados: {self.personas_visitantes} : {self.placas_autorizadas} Fecha: {self.fecha_creacion} "


    #manejamos el guardado de alguna mascota por alguna seguridad aparte etc
    def save (self, *args , **kwargs):
        #valdacion personalizada para guardar la visita
        if self.personas_visitantes:
            pass #si se cumple alguna de esta se ejecuta este codigo
        super().save(*args, **kwargs)
    
    class meta:#legible para el usuario en admin
        
        indexes = [
            "personas_autorizadas", "placas_autorizadas"
        ]
        
        # Esto cambiará cómo se muestra en el admin
        verbose_name = "Registro de Visita"
        verbose_name_plural = "Registros de Visitas"
        
# Tabla RegistroAutomoviles
class RegistroAutomovil(models.Model):
    
    #Recordar la logica del proyecto general y no es la de la aplicacion de los condominos
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    auto = models.CharField(max_length=100, null=True, blank=True)
    imagen = models.ImageField(upload_to='autos/', null=True , blank=True)
    caracteristicas = models.TextField(null=True, blank=True)
    placa = models.CharField(max_length=50, null=False)
    fecha_creada_auto = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f" {self.usuario.username}  Marca {self.auto} : Placa {self.placa} : {self.caracteristicas}  "


    #manejamos el guardado de alguna mascota por alguna seguridad aparte etc
    def save (self, *args , **kwargs):
        #valdacion personalizada para guardar la visita
        if self.auto:
            pass #si se cumple alguna de esta se ejecuta este codigo
        super().save(*args, **kwargs)
    
    class meta:#legible para el usuario en admin
        
        indexes = [
            "auto", "placa"
        ]
        
        verbose_name="Vehículo"
        verbose_name_plural="Vehículos"
        
    
# Tabla RegistroMascotas
class RegistroMascota(models.Model):
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100,null=False )
    foto = models.ImageField(upload_to='mascotas/' , null=True , blank=True)
    caracteristicas = models.TextField(null=True , blank=True)
    fecha_creado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f" {self.usuario.username} Mascota {self.nombre} : {self.caracteristicas} "


    #manejamos el guardado de alguna mascota por alguna seguridad aparte etc
    def save (self, *args , **kwargs):
        #valdacion personalizada para guardar la visita
        if self.nombre:
            pass #si se cumple alguna de esta se ejecuta este codigo
        super().save(*args, **kwargs)
    
    class meta:#legible para el usuario en admin
        
        indexes = [
            "nombre", "caracteristicas"
        ]
        
        verbose_name="Mascota"
        verbose_name_plural="Mascotas"
        
class RegistroReporte(models.Model):
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    reporte = models.TextField(blank=False, null=False)
    fecha_creado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f" {self.usuario.username} Reporte:{self.reporte}  Fecha:{self.fecha_creado} "


    #manejamos el guardado de alguna mascota por alguna seguridad aparte etc
    def save (self, *args , **kwargs):
        #valdacion personalizada para guardar la visita
        if self.reporte:#si se cumple alguna de esta se ejecuta este codigo
            pass 
        super().save(*args, **kwargs)
    
    class meta:#legible para el usuario en admin
        
        indexes = [
            "reporte", "fecha_creado"
        ]
        
        verbose_name="Reporte"
        verbose_name_plural="Reportes"
        


