from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required #Decorador de login
from django.http import HttpResponse



# Create your views here.
#utilizaremos decoradores para manejar que el usuario este logeado en el sistema general del servidor para poder acceder a esta pagina
@login_required #Podemos utilizarlo en todas las funciones del proyecto, pero realizo pruebas de uso de diferentes auth en el html con jin {{ if is_auth }} etc
def inicio(request):#prueba de inicio pero la pagina 1 es la principal para el proyecto general
    return HttpResponse("Hola aca estamos logeados : --> Al crear tu cuenta tienes acceso a las demas aplicaciones del sistema Portafolio")


def crear_cuenta(request):
    try:
        if request.method == "POST":
            formulario = UserCreationForm(request.POST)
            if formulario.is_valid():
                formulario.save()
                return redirect("login")
        else:
            formulario = UserCreationForm()
        return render(request, "accounts/signup.html", {"form": formulario})
    except Exception as e:
        error = str(e)
        print(f"Muestro en el servidor el error: {error}")
        return HttpResponse(f"Hola, ha ocurrido un problema. Por favor, inténtalo más tarde. Error: {error}")

#esto es lo unico que haremos con el usuario general pasamos a las urls creamos el urls.py en la app