

from django.db import transaction  # Importar el módulo de transacciones de Django




from .models import Marca, Modelo, Categoria, AnioAuto
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Repuesto, Comentario

from .models import Carrito, ItemCarrito, ItemOrden,Orden
from django.db.models import F

from django.db.models import Q
from django.core.paginator import Paginator
from urllib.parse import urlencode
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render

def lista_repuestos(request):
    # Obtener parámetros de búsqueda
    filters = {
        'query': request.GET.get('q', ''),
        'marca_id': str(request.GET.get('marca', '')),
        'modelo_id': str(request.GET.get('modelo', '')),
        'anio_id': str(request.GET.get('anio', '')),
        'categoria_id': str(request.GET.get('categoria', ''))
    }
    
    # Consulta base para repuestos y ofertas
    repuestos = Repuesto.objects.all().order_by('codigo')
    ofertas = Repuesto.objects.filter(en_oferta=True).order_by('nombre')
    ofertas_especiales = Repuesto.objects.filter(oferta_especial=True).order_by('nombre')
    
    # Aplicar filtros a los repuestos
    if filters['query']:
        repuestos = repuestos.filter(
            Q(nombre__icontains=filters['query']) |
            Q(modelos_anios_compatibles__modelo__nombre__icontains=filters['query']) |
            Q(modelos_anios_compatibles__modelo__marca__nombre__icontains=filters['query'])
        ).distinct()
    
    if filters['marca_id']:
        repuestos = repuestos.filter(modelos_anios_compatibles__modelo__marca__id=filters['marca_id'])
    if filters['modelo_id']:
        repuestos = repuestos.filter(modelos_anios_compatibles__modelo__id=filters['modelo_id'])
    if filters['anio_id']:
        repuestos = repuestos.filter(modelos_anios_compatibles__anios__id=filters['anio_id'])
        
    if filters['categoria_id']:
        repuestos = repuestos.filter(categorias__id=filters['categoria_id'])
    
    # Paginación de repuestos principales
    paginator = Paginator(repuestos.distinct(), 14)
    page_number = request.GET.get('page', '1')
    page_obj = paginator.get_page(page_number)
    
    # Paginación de ofertas
    offers_paginator = Paginator(ofertas.distinct(), 6)
    offers_page_number = request.GET.get('offers_page', '1')
    offers_page = offers_paginator.get_page(offers_page_number)
    
    # Paginación de ofertas especiales
    especiales_paginator = Paginator(ofertas_especiales.distinct(), 5)
    especiales_page_number = request.GET.get('especiales_page', '1')
    especiales_page = especiales_paginator.get_page(especiales_page_number)
    
    # Construir query strings manteniendo el estado de todas las paginaciones
    query_params = request.GET.copy()
    
    # Query string para repuestos principales
    main_query_params = query_params.copy()
    if 'page' in main_query_params:
        del main_query_params['page']
    if 'offers_page' in query_params:
        main_query_params['offers_page'] = query_params['offers_page']
    if 'especiales_page' in query_params:
        main_query_params['especiales_page'] = query_params['especiales_page']
    main_query_string = main_query_params.urlencode()
    
    # Query string para ofertas
    offers_query_params = query_params.copy()
    if 'offers_page' in offers_query_params:
        del offers_query_params['offers_page']
    if 'page' in query_params:
        offers_query_params['page'] = query_params['page']
    if 'especiales_page' in query_params:
        offers_query_params['especiales_page'] = query_params['especiales_page']
    offers_query_string = offers_query_params.urlencode()
    
    # Query string para ofertas especiales
    especiales_query_params = query_params.copy()
    if 'especiales_page' in especiales_query_params:
        del especiales_query_params['especiales_page']
    if 'page' in query_params:
        especiales_query_params['page'] = query_params['page']
    if 'offers_page' in query_params:
        especiales_query_params['offers_page'] = query_params['offers_page']
    especiales_query_string = especiales_query_params.urlencode()
    
    # Manejo seguro del carrito
    cantidad_car = 0
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user, activo=True).first()
        if carrito:
            cantidad_car = carrito.items.count()
    
    # Contexto para la plantilla
    context = {
        'page_obj': page_obj,
        'offers_page': offers_page,
        'especiales_page': especiales_page,
        'marcas': Marca.objects.all().order_by('nombre'),
        'modelos': Modelo.objects.all().order_by('nombre'),
        'categorias': Categoria.objects.all().order_by('nombre'),
        'anios': AnioAuto.objects.all().order_by('-anio'),
        
        'cantidad_car': cantidad_car,
        'query': filters['query'],
        'selected_marca': filters['marca_id'],
        'selected_modelo': filters['modelo_id'],
        'selected_anio': filters['anio_id'],
        'selected_categoria': filters['categoria_id'],
        'main_query_string': main_query_string,
        'offers_query_string': offers_query_string,
        'especiales_query_string': especiales_query_string,
        'current_page': page_number,
        'current_offers_page': offers_page_number,
        'current_especiales_page': especiales_page_number
    }
    
    return render(request, 'repuestos/lista_repuestos.html', context)


@login_required
def actualizar_cantidad(request, item_id):
    item_carrito = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    if request.method == 'POST':
        nueva_cantidad = int(request.POST.get('cantidad'))
        if nueva_cantidad > 0 and nueva_cantidad <= item_carrito.repuesto.stock:
            item_carrito.cantidad = nueva_cantidad
            item_carrito.save()
    return redirect('ver_carrito')

@login_required
def eliminar_item(request, item_id):
    item = get_object_or_404(ItemCarrito, 
                id=item_id, 
                carrito__usuario=request.user,
                carrito__activo=True
            )
    if request.method == 'POST':
        try:
            item.delete()
            messages.success(request, 'Producto eliminado del carrito exitosamente')
        except:
            messages.error(request, 'Error al eliminar el producto del carrito')
    
    return redirect('ver_carrito')



@login_required
def agregar_al_carrito(request, repuesto_id):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        repuesto = get_object_or_404(Repuesto, id=repuesto_id)
        
        if repuesto.stock < cantidad:
            messages.error(request, 'No hay suficientes productos en stock')
            return redirect('detalle_repuesto', pk=repuesto_id)

        carrito, _ = Carrito.objects.get_or_create(
            usuario=request.user,
            activo=True
        )

        item, created = ItemCarrito.objects.get_or_create(
            carrito=carrito,
            repuesto=repuesto,
            defaults={'cantidad': cantidad}
        )

        if not created:
            item.cantidad = F('cantidad') + cantidad
            item.save()

        messages.success(request, 'Producto agregado')
        return redirect('ver_carrito')

    return redirect('detalle_repuesto', pk=repuesto_id)



@login_required
def ver_carrito(request):
    # Intentar obtener el carrito activo del usuario
    carrito = Carrito.objects.filter(usuario=request.user, activo=True).first()
    
    # Si no hay un carrito activo, crear uno nuevo
    if not carrito:
        carrito = Carrito.objects.create(usuario=request.user, activo=True)
    
    # Contar la cantidad de ítems en el carrito
    cantidad_car = carrito.items.count()

    # Guardar los ítems del carrito en la sesión
    cart_items = [
        {
            'code_reference': item.repuesto.codigo,
            'name': item.repuesto.nombre,
            'quantity': item.cantidad,
            'price': float(item.subtotal() / item.cantidad)  # Convertir Decimal a float
        }
        for item in carrito.items.all()
    ]
    request.session['cart_items'] = cart_items

    # Renderizar la plantilla del carrito con los datos necesarios
    return render(request, 'repuestos/carrito.html', {
        'carrito': carrito,
        'cantidad_car': cantidad_car,
    })




def detalle_repuesto(request, pk):
    repuesto = get_object_or_404(Repuesto, pk=pk)
    
    # Manejo seguro del carrito
    cantidad_car = 0
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user, activo=True).first()
        if carrito:
            cantidad_car = carrito.items.count()
    
    # Obtener los años compatibles de los modelos asociados al repuesto
    anios_compatibles = {anio for modelo_anio in repuesto.modelos_anios_compatibles.all() for anio in modelo_anio.anios.all()}
    return render(request, 'repuestos/detalle_repuesto.html', {
        'repuesto': repuesto,
        'cantidad_car': cantidad_car,
        'anios_compatibles': anios_compatibles
    })











@login_required
def agregar_comentario(request, repuesto_id):
    if request.method == 'POST':
        repuesto = get_object_or_404(Repuesto, id=repuesto_id)
        calificacion = request.POST.get('calificacion')
        texto = request.POST.get('texto')

        # Verificar si el usuario ya comentó
        comentario_existente = Comentario.objects.filter(
            repuesto=repuesto,
            usuario=request.user
        ).first()

        if comentario_existente:
            messages.error(request, 'Ya has comentado este repuesto')
        else:
            Comentario.objects.create(
                repuesto=repuesto,
                usuario=request.user,
                calificacion=calificacion,
                texto=texto
            )
            messages.success(request, 'Comentario agregado exitosamente')

    return redirect('detalle_repuesto', pk=repuesto_id)




def categoria_lista(request):
    categories = Categoria.objects.all().order_by("nombre")
    return render(request, 'repuestos/category_list.html', {'categorias': categories})

def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Repuesto.objects.filter(categorias=categoria).order_by('nombre')
    
    # Filtros
    query = request.GET.get('q', '')
    if query:
        productos = productos.filter(nombre__icontains=query)
    
    # Ordenamiento
    orden = request.GET.get('orden', '')
    if orden == 'precio_bajo':
        productos = productos.order_by('precio')
    elif orden == 'precio_alto':
        productos = productos.order_by('-precio')
    elif orden == 'nuevos':
        productos = productos.order_by('-fecha_creacion')
    
    # Paginación
    paginator = Paginator(productos, 12)  # 12 productos por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'categoria': categoria,
        'page_obj': page_obj,
        'query': query,
        'orden': orden,
        'total_productos': productos.count()
    }
    
    return render(request, 'repuestos/categoria_template.html', context)













@login_required
def actualizar_cantidad(request, item_id):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
        
        if cantidad <= 0:
            item.delete()
            messages.success(request, 'Item eliminado del carrito')
        else:
            if item.repuesto.stock < cantidad:
                messages.error(request, 'No hay suficiente stock disponible')
            else:
                item.cantidad = cantidad
                item.save()
                messages.success(request, 'Cantidad actualizada')

    return redirect('ver_carrito')

@login_required
def vaciar_carrito(request):
    if request.method == 'POST':
        carrito = get_object_or_404(Carrito, usuario=request.user, activo=True)
        carrito.items.all().delete()
        messages.success(request, 'Carrito vaciado exitosamente')
    
    return redirect('ver_carrito')




# Importamos el decorador login_required para asegurar que solo usuarios autenticados accedan
@login_required
def procesar_pago(request):
    # Comprobamos que el método de la solicitud sea POST
    if request.method == 'POST':
        # Obtenemos el carrito del usuario que está activo
        carrito = get_object_or_404(Carrito, usuario=request.user, activo=True)
        
        # Verificamos el stock de cada ítem antes de procesar
        for item in carrito.items.all():
            # Si el stock es insuficiente, mostramos un mensaje de error y redirigimos al carrito
            if item.repuesto.stock < item.cantidad:
                messages.error(request, f'No hay suficiente stock de {item.repuesto.nombre}')
                return redirect('ver_carrito')
        
        try:
            with transaction.atomic():  # Usar una transacción atómica para asegurar la integridad de los datos
                # Creamos una nueva orden para el usuario con el total del carrito
                orden = Orden.objects.create(
                    usuario=request.user,
                    total=carrito.total()
                )
                
                # Guardamos cada ítem del carrito en la orden y actualizamos el stock
                for item in carrito.items.all():
                    ItemOrden.objects.create(
                        orden=orden,
                        repuesto=item.repuesto,
                        cantidad=item.cantidad,
                        precio_unitario=item.repuesto.precio,
                        subtotal=item.subtotal()
                    )
                    # Restamos la cantidad del ítem al stock del repuesto
                    item.repuesto.stock -= item.cantidad
                    item.repuesto.save()
                
                # Vaciamos todos los ítems del carrito actual
                carrito.items.all().delete()
                
                # Mostramos un mensaje de éxito y redirigimos a la lista de repuestos
                messages.success(request, 'Pago procesado exitosamente')
                return redirect('gyna')
        
        except Exception as e:
            # Manejo de errores
            messages.error(request, f'Error al procesar el pago: {e}')
    
    # Si no es una solicitud POST, redirigimos al carrito
    return redirect('ver_carrito')



def ver_mas_especiales(request):
    # Query base
    especiales = Repuesto.objects.filter(oferta_especial=True)
    
    # Búsqueda
    query = request.GET.get('q', '')
    if query:
        especiales = especiales.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        )
    
    # Filtro por descuento
    descuento = request.GET.get('descuento', '')
    if descuento:
        try:
            descuento_valor = int(descuento)
            especiales = especiales.filter(porcentaje_descuento__gte=descuento_valor)
        except ValueError:
            pass
    
    # Ordenamiento
    orden = request.GET.get('orden', '')
    if orden == 'precio_bajo':
        especiales = especiales.order_by('precio')
    elif orden == 'precio_alto':
        especiales = especiales.order_by('-precio')
    elif orden == 'nuevos':
        especiales = especiales.order_by('-fecha_creacion')
    elif orden == 'calificacion':
        especiales = list(especiales)
        especiales.sort(key=lambda x: x.promedio_calificacion(), reverse=True)
    
    context = {
        'especiales': especiales,
        'query': query,
        'orden': orden,
        'descuento': descuento,
    }
    
    return render(request, 'repuestos/ver_mas_especiales.html', context)