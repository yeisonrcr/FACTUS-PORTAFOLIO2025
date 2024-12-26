from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required #Decorador de login
from django.http import HttpResponse



# Create your views here.
#utilizaremos decoradores para manejar que el usuario este logeado en el sistema general del servidor para poder acceder a esta pagina
@login_required #Podemos utilizarlo en todas las funciones del proyecto, pero realizo pruebas de uso de diferentes auth en el html con jin {{ if is_auth }} etc
def inicio(request):#prueba de inicio pero la pagina 1 es la principal para el proyecto general
    return HttpResponse("Hola aca estamos logeados : --> Al crear tu cuenta tienes acceso a las demas aplicaciones del sistema Portafolio")




def crear_cuenta(request):#funcion para crear una cuenta en django admin por defecto 
    try:#validacion de erroes   
        if request.method == "POST": #Si es la peticion POST: ENVIAN INFORMACION 
            formulario = UserCreationForm(request.POST) #Extraigo el formulario para crear un usuario en django system
            if formulario.is_valid(): #si el formulario es valido
                #entro aca y lo guardo 
                formulario.save() #puedes realizar un cleaned_data para limpiar datos y seguridad
                
                #implementar seguridad extras     
                return redirect("login")
        
        else: #si el POST, solo presento el formulario de creacion
            formulario = UserCreationForm()#creo el formulario vacio)
            print(formulario)
        return render(request, "accounts/signup.html", {"form":formulario})
    except Exception as e:#manejo de errores
        error = str(e)
        print("Muestro en el servidor el error: " +  str(error)) #forma sencilla de mostrara el error de servidor
    
    return HttpResponse(f"Hola ha ocurrido un problema, por favor intentalo mas tarde    Error: {error}")
    
#esto es lo unico que haremos con el usuario general pasamos a las urls creamos el urls.py en la app