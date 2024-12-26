from django.shortcuts import render

# Create your views here.


#defino pagina 1 y pagina 2 de la app portafolio
def index(request):
    try:
        username = None
        #validar proyecto general LOG
        if request.user.username:
            username = request.user.username
        
    except Exception as e: #manejo de errores
        print(f"error: {e}")
    return render (request, "portafolio/index.html", {"username":username, })
    #retorno a la pagina index con los datos de usuario

def proyecto(request):#funcion contralador para las vistas del proyecto página 2
    return render (request, "portafolio/cv.html")
