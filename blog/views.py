from django.shortcuts import render, HttpResponse
from .models import Blog
from django.core.paginator import Paginator
import re

def extract_video_id(url):
    match = re.search(r'youtu(?:\.be|be\.com)\/(?:watch\?v=|embed\/)([a-zA-Z0-9_-]+)', url)
    return match.group(1) if match else None



def blog(request):
    if request.method == 'POST':
        # Aquí iría el manejo del caso POST, por ejemplo, para manejar formularios o acciones de los usuarios.
        return render(request, 'blog/blog.html')

    elif request.method == 'GET':
        texto_caract = Blog.objects.all().order_by('-fecha_creacion')  # Obtener todos los blogs
        paginator = Paginator(texto_caract, 5)  # Mostrar 5 blogs por página
        page_number = request.GET.get('page')  # Obtener el número de página desde la URL
        page_obj = paginator.get_page(page_number)  # Obtener la página correspondiente
        
        # Extraer el ID del video de YouTube
            
        context = {
            'page_obj': page_obj,  # Pasamos la página de blogs al template
        }

        return render(request, 'blog/blog.html', context)


    else:
        # Si el método no es GET ni POST, se devuelve un error 405 (Método no permitido)
        return HttpResponse(status=405)
