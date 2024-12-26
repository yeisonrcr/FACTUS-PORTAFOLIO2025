#Utilizaré vistas basadas en clases para aprovechar la herencia y mantener un código más organizado.
#vistas por defecto
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, View
)

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin #mixins utilizados, explicación en el archivo info
from django.urls import reverse_lazy #definir URLs por adelantado 

#consultas complejas a la base de datos combinar usando operadores logicos y demas
from django.db.models import Q 

from django.shortcuts import get_object_or_404, redirect, render #rendings
from django.shortcuts import reverse
from django.contrib import messages #messager front

#mis archivos
from .models import Tienda, Producto, Categoria, Carrito, ItemCarrito, Provincia, Canton, Distrito
from .forms import TiendaForm, ProductoForm, CarritoForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#manejar paginación de tablas a 10 campos, rendimiento.


    
    
from django.db import transaction
from django.db.models import F



#funciones api
from django.http import JsonResponse

def get_cantones(request): 
    provincia_id = request.GET.get('provincia_id') 
    cantones = Canton.objects.filter(provincia_id=provincia_id).order_by('nombre') 
    return JsonResponse(list(cantones.values('id', 'nombre')), safe=False) 

def get_distritos(request): 
    canton_id = request.GET.get('canton_id') 
    distritos = Distrito.objects.filter(canton_id=canton_id).order_by('nombre') 
    return JsonResponse(list(distritos.values('id', 'nombre')), safe=False)



class TiendaListView(ListView):
    """
    Vista para listar todas las tiendas disponibles
    Implementa búsqueda y filtrado
    """
    model = Tienda
    context_object_name = 'tiendas'
    paginate_by = 10  # Paginación de 10 tiendas

    def get_queryset(self):
        """
        Método para implementar búsqueda y filtrado de tiendas
        """
        queryset = Tienda.objects.all()

        try:
            # Búsqueda por términos
            query = self.request.GET.get('q')
            if query:
                queryset = queryset.filter(
                    Q(nombre__icontains=query) |
                    Q(provincia__nombre__icontains=query) |
                    Q(canton__nombre__icontains=query)
                )

            # Filtrado por provincia
            provincia = self.request.GET.get('provincia')
            if provincia:
                queryset = queryset.filter(provincia__nombre=provincia)

        except Exception as e:
            raise e

        # Asegurar orden antes de retornar
        return queryset.order_by('-fecha_creacion')  # Ordenar por fecha de creación descendente

    def get_context_data(self, **kwargs):
        """
        Añade información adicional al contexto
        """
        context = super().get_context_data(**kwargs)
        context['provincias'] = Provincia.objects.all()  # Listado de provincias para filtros
        return context

class TiendaDetailView(DetailView):
    """
    Vista de detalle para una tienda específica
    Muestra productos de la tienda con paginación
    """
    model = Tienda
    #template_name = 'ecommerce/tienda_detail.html'
    context_object_name = 'tienda'
    

    def get_context_data(self, **kwargs):
        """
        Añade productos de la tienda con filtrado y paginación
        """
        context = super().get_context_data(**kwargs)
        try:
            
            # Obtener productos de la tienda
            productos = self.object.productos.all()
            
            # Filtrado por categoría
            categoria = self.request.GET.get('categoria')
            if categoria:
                productos = productos.filter(categoria__slug=categoria)
            
            # Búsqueda, con el query del ´q y filtramos si contenemos en dicho dato en el array-productos
            query = self.request.GET.get('q')
            if query:
                productos = productos.filter(
                    Q(nombre__icontains=query) | 
                    Q(detalles__icontains=query)
                )
            
            # Paginación
            paginator = Paginator(productos, 10)  # 10 productos por página
            page_number = self.request.GET.get('page')
            context['productos'] = paginator.get_page(page_number)
            
            # Categorías de la tienda
            context['categorias'] = Categoria.objects.filter(
                producto__tienda=self.object
            ).distinct()
            
            

        except Exception as e:
            raise e
                
        return context
    
    
    

class ProductoDetailView(DetailView):
    """
    Vista de detalle para un producto específico
    Incluye lógica para agregar al carrito
    """
    model = Producto
    context_object_name = 'producto'

    def get_context_data(self, **kwargs):
        """
        Añade formulario de carrito al contexto
        """
        context = super().get_context_data(**kwargs)
        try:
            context['carrito_form'] = CarritoForm(
                initial={'producto_id': self.object.id}
            )
        except Exception as e:
            raise e
            
        return context

    def validar_stock(self, producto, cantidad, item_carrito=None):
        """
        Función que valida si hay suficiente stock
        Si ya existe un ítem en el carrito, se suman las cantidades
        """
        stock_disponible = producto.stock

        # Si ya existe un item en el carrito, consideramos la cantidad total
        if item_carrito:
            cantidad_total = item_carrito.cantidad + cantidad
        else:
            cantidad_total = cantidad
        
        # Validación del stock
        if cantidad_total > stock_disponible:
            # Si no hay suficiente stock, se devuelve False y la cantidad restante disponible
            return False, stock_disponible - (item_carrito.cantidad if item_carrito else 0)  
        return True, stock_disponible

    def post(self, request, *args, **kwargs):
        """
        Maneja la adición de productos al carrito
        """
        self.object = self.get_object()  # Obtenemos el objeto del post
        carrito_form = CarritoForm(request.POST)
        try:
            if carrito_form.is_valid():
                cantidad = carrito_form.cleaned_data['cantidad']

                # Usamos una transacción para garantizar que las operaciones sean atómicas
                with transaction.atomic():
                    # Usamos select_for_update para bloquear el producto mientras modificamos el stock
                    producto = Producto.objects.select_for_update().get(id=self.object.id)

                    # Validar si el stock disponible es suficiente para la cantidad solicitada
                    is_valid, remaining_stock = self.validar_stock(producto, cantidad)
                    
                    if not is_valid:
                        # Si no hay suficiente stock, mostramos un mensaje de error
                        messages.error(request, f'No hay suficiente stock para agregar {cantidad} del producto {producto.nombre}. Solo quedan {remaining_stock} unidades disponibles.')
                        return redirect('carrito')  # Redirigir al carrito sin agregar más productos

                    # Obtener o crear carrito para esta tienda
                    carrito, created = Carrito.objects.get_or_create(
                        usuario=request.user,
                        tienda=producto.tienda
                    )

                    # Verificar si el producto ya está en el carrito
                    item_carrito, created = ItemCarrito.objects.get_or_create(
                        carrito=carrito,
                        producto=producto,
                        defaults={
                            'cantidad': cantidad,
                            'precio_unitario': producto.precio
                        }
                    )

                    # Si el producto ya está en el carrito, actualizar la cantidad
                    if not created:
                        cantidad_total_en_carrito = item_carrito.cantidad + cantidad
                        # Validar si la nueva cantidad excede el stock disponible
                        is_valid, remaining_stock = self.validar_stock(producto, cantidad, item_carrito)
                        if not is_valid:
                            messages.error(request, f'No hay suficiente stock para agregar {cantidad} más del producto {producto.nombre}. Solo quedan {remaining_stock} unidades disponibles.')
                            return redirect('carrito')  # Redirigir al carrito sin agregar más productos

                        item_carrito.cantidad = cantidad_total_en_carrito  # Actualizamos la cantidad del carrito
                        item_carrito.save()  # Guardamos los cambios

                    #else:
                        # Si el producto no está en el carrito, actualizamos el stock
                        #producto.stock -= cantidad
                        #producto.save()  # Guardamos los cambios en el stock del producto

                    # Mostrar mensaje de éxito si todo es correcto
                    messages.success(request, f'{producto.nombre} agregado al carrito.')

                # Después de una operación exitosa, redirigimos al carrito
                return redirect('carrito')

        except Exception as e:
            # Manejo de errores más específico, mostrando mensaje de error al usuario
            messages.error(request, f'Ocurrió un error al agregar el producto al carrito: {str(e)}')
            return redirect('carrito')

        # Si hay un error, simplemente hacemos el GET para mostrar la página
        return self.get(request, *args, **kwargs)














    
    
    

#Crear tienda, con el superuser logeado VERIFICAR LA SEGURIDAD QUE SOLO UN SUPERUSER PUEDE CREAR TIENDAS 
class CrearTiendaView(LoginRequiredMixin, UserPassesTestMixin, CreateView): #vistas por defecto de Django, verificar versiones y documentación
    """
    Vista para crear una nueva tienda
    Solo accesible por superusuarios
    """
    model = Tienda
    form_class = TiendaForm
    #template_name = 'ecommerce/crear_tienda.html'
    success_url = reverse_lazy('tienda_list') #urls por adelantado 

    def test_func(self):
        """
        Verifica que solo superusuarios puedan crear tiendas
        """
        return self.request.user.is_superuser

    def form_valid(self, form):
        """
        Asigna el propietario de la tienda
        """
        form.instance.propietario = self.request.user
        return super().form_valid(form)

#agregar nuevo producto, y su seguridad
class CrearProductoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Vista para crear productos en una tienda
    Solo el propietario de la tienda puede agregar productos
    """
    model = Producto #llamo el modelo
    form_class = ProductoForm #llamo el formulario para guardar datos al modelo
    #template_name = 'ecommerce/crear_producto.html' #utilizo el templates settings de django

    
    #seguridad
    def test_func(self):
        """
        Verifica que solo el propietario de la tienda pueda agregar productos
        """
        #control de agregado de productos
        tienda = get_object_or_404(Tienda, pk=self.kwargs['tienda_pk']) #seguridad
        
        return self.request.user == tienda.propietario #retorno dueño del producto

    
    def form_valid(self, form):
        """
        Asigna la tienda al producto manual por seguridad objetos
        """
        tienda = get_object_or_404(Tienda, pk=self.kwargs['tienda_pk']) 
        print(str(tienda))
        
        form.instance.tienda = tienda
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirige a la lista de productos de la tienda
        """
        return reverse_lazy('tienda_detail', kwargs={'slug': self.object.tienda.slug})
        #return reverse_lazy('tienda_detail', kwargs={'slug': self.object.slug}) Estaba obteniendo el slug del producto y no el de la tienda
        
        #recordar que manejo slug para las url limpias pero puedes usar el PK de kwars para manejo como en los condominios
        
        #return reverse_lazy('tienda_detail', kwargs={'slug': self.kwargs['tienda_slug']})
        
        


"""
    Consideraciones Importantes

        Validación de Stock: En la vista, se valida que la cantidad no supere el stock disponible.
        Mensajes de Usuario: Se usan mensajes de Django para notificar acciones exitosas o errores.
        Seguridad: Solo el usuario propietario puede modificar su propio carrito.

"""






class CarritoView(LoginRequiredMixin, View):
    """
    Vista para gestionar el carrito de compras.
    Proporciona las funcionalidades para listar, actualizar, vaciar y eliminar ítems del carrito.
    """
    template_name = 'tiendas/carrito.html'  # Plantilla asociada a esta vista
    items_por_pagina = 10  # Número de items por página para la paginación


    def get(self, request):
        """
        Maneja las solicitudes GET.
        Muestra todos los carritos del usuario autenticado con sus items paginados.
        """
        carritos = Carrito.objects.filter(usuario=request.user).prefetch_related('items__producto')

        carritos_paginados = self._serializar_carritos(carritos, request)
        total_precio = 0

        for carrito in carritos:
            for item in carrito.items.all():  # Iterar sobre los ítems de cada carrito
                try:
                    producto = item.producto
                    cantidad = item.cantidad
                    subtotal = producto.precio * cantidad

                    total_precio += subtotal
                except Exception as e:
                    self.agregar_mensaje(request, 'error', f'Errores al realizar la compra: {e}')
        
        return render(request, self.template_name, {
            'carritos_paginados': carritos_paginados,
            'total_precio': total_precio,
            
        })






    #METODOS POST ()
    def post(self, request):
        """
        Maneja las solicitudes POST.
        Procesa las acciones de actualizar cantidad, vaciar carrito y eliminar ítems.
        """
        try:
            # Verificar qué acción se está solicitando
            if 'actualizar_cantidad' in request.POST:
                return self._actualizar_cantidad(request)
            elif 'vaciar_carrito' in request.POST:
                return self._vaciar_carrito(request)
            elif 'eliminar_item' in request.POST:
                return self._eliminar_item(request)
            
            elif 'realizar_compra' in request.POST:
                return self._realizar_compra(request)
            
            
        except Exception as e:
            # Manejo general de errores
            self.agregar_mensaje(request, 'error', f'Error al procesar el carrito: {str(e)}')
        return redirect('carrito')

    def _serializar_carritos(self, carritos, request):
        """
        Serializa los carritos para incluir la paginación de sus items.
        """
        carritos_paginados = []  # Lista para almacenar los carritos con items paginados

        for carrito in carritos:
            # Obtener los items asociados al carrito
            items = carrito.items.all()

            # Configurar la paginación
            paginator = Paginator(items, self.items_por_pagina)
            page = request.GET.get(f'page_carrito_{carrito.id}', 1)

            try:
                # Obtener los items de la página solicitada
                items_pagina = paginator.page(page)
            except PageNotAnInteger:
                items_pagina = paginator.page(1)  # Página predeterminada
            except EmptyPage:
                items_pagina = paginator.page(paginator.num_pages)  # Última página

            # Crear un diccionario con el carrito y sus items paginados
            carrito_paginado = {
                'carrito': carrito,
                'items': items_pagina,
                'total_paginas': paginator.num_pages,
                'pagina_actual': items_pagina.number
            }
            carritos_paginados.append(carrito_paginado)

        return carritos_paginados
    
    
    
    

    def _actualizar_cantidad(self, request):
        """
        Actualiza la cantidad de un ítem en el carrito.
        """
        item_id = request.POST.get('item_id')
        nueva_cantidad = request.POST.get('cantidad')

        try:
            # Recuperar el ítem y validar que pertenece al usuario
            item = ItemCarrito.objects.get(id=item_id, carrito__usuario=request.user)
            """Ese ítem pertenece al carrito correcto.
                Ese carrito pertenece al usuario correcto al manejar sistema de seguridad con el sistema de registro."""
            producto = item.producto #de todo el item obtengo los productos de la clase 

            # Validar el stock del producto
            if int(nueva_cantidad) <= producto.stock + 1:
                item.cantidad = nueva_cantidad
                item.save()  # Guardar los cambios
                self.agregar_mensaje(request, 'success', 'Cantidad actualizada correctamente')
            else:
                self.agregar_mensaje(request, 'error', f'Solo hay {producto.stock} unidades disponibles')
        except ItemCarrito.DoesNotExist:
            self.agregar_mensaje(request, 'error', 'El ítem no existe')

        return redirect('carrito')

    def _vaciar_carrito(self, request):
        """
        Vacía completamente un carrito, eliminando todos sus ítems.
        """
        carrito_id = request.POST.get('carrito_id')
        try:
            # Recuperar el carrito asociado al usuario
            carrito = Carrito.objects.get(id=carrito_id, usuario=request.user)
            carrito.items.all().delete()  # Eliminar todos los ítems
            carrito.delete()  # Eliminar el carrito
            self.agregar_mensaje(request, 'success', 'Carrito eliminado')
        except Carrito.DoesNotExist:
            self.agregar_mensaje(request, 'error', 'El carrito no existe')

        return redirect('carrito')
    
        
    def _eliminar_item(self, request):
        """
        Elimina un ítem específico del carrito.
        Si el carrito queda vacío, también se elimina.
        """
        item_id = request.POST.get('item_id')
        carrito_id = request.POST.get('carrito_id')

        try:
            # Recuperar el ítem y validar que pertenece al usuario
            item = ItemCarrito.objects.get(id=item_id, carrito__id=carrito_id, carrito__usuario=request.user)
            item.delete()  # Eliminar el ítem

            # Verificar si el carrito quedó vacío
            carrito = Carrito.objects.get(id=carrito_id, usuario=request.user)
            if not carrito.items.exists():
                carrito.delete()  # Eliminar el carrito vacío
                self.agregar_mensaje(request, 'success', 'El producto fue eliminado y el carrito también, ya que quedó vacío.')
            else:
                self.agregar_mensaje(request, 'success', 'Producto eliminado del carrito.')
        except ItemCarrito.DoesNotExist:
            self.agregar_mensaje(request, 'error', 'El ítem no existe')
        except Carrito.DoesNotExist:
            self.agregar_mensaje(request, 'error', 'El carrito no existe')

        return redirect('carrito')

    @staticmethod #metodo estatico para la clase Carrito Mejorando codigo limpio
    #función personalizada que encapsula la lógica de agregar mensajes al request.
    def agregar_mensaje(request, tipo, mensaje):
        """
        Agrega un mensaje al sistema de mensajes de Django.
        :param request: Objeto de la solicitud.
        :param tipo: Tipo de mensaje ('success' o 'error').
        :param mensaje: Contenido del mensaje.
        """
        if tipo == 'success':
            messages.success(request, mensaje)
        elif tipo == 'error':
            messages.error(request, mensaje)





    def _realizar_compra(self, request):
        try:
            # Obtener el ID del carrito desde el formulario
            carrito_id = request.POST.get('carrito_id')
            
            # Verificar que se haya recibido un carrito_id válido, sin embargo ya esta implementada la seguridad, de no mostrar carritos vacios
            if not carrito_id:
                self.agregar_mensaje(request, "error" ,'No se especificó un carrito.')
                return redirect('carrito')  # Redirigir a la vista del carrito si no hay carrito_id

            try:
                # Buscar en la DB, el carrito correspondiente con usuario logeado, seguridad de tomar el carrito
                carrito = Carrito.objects.get(id=carrito_id, usuario=request.user)
                
                # Obtener todos los ítems del carrito
                items = carrito.items.all()
                
                if not items.exists():
                    self.agregar_mensaje(request, "error",'El carrito está vacío.' )
                    
                    return redirect('carrito')  # Redirigir a la vista del carrito si está vacío

            except Carrito.DoesNotExist:
                
                self.agregar_mensaje(request, "error" ,'El carrito no existe o no pertenece al usuario.')
                                     
                return redirect('carrito')  # Redirigir a la vista del carrito si no existe

            
            # Variables para almacenar detalles del producto y el precio total
            productos_detalles = []
            total_precio = 0
            
            

            # Iterar sobre los ítems del carrito
            for item in items:
                try:
                    producto = item.producto  # Producto asociado al ítem
                    cantidad = item.cantidad  # Cantidad seleccionada
                        
                    # Verificar si hay suficiente stock
                    if producto.stock < cantidad:
                        self.agregar_mensaje(request,"error", f'No hay suficiente stock para {producto.nombre}')
                        return redirect('carrito')
                    
                    # Restar la cantidad del stock, validar atómicos
                    producto.stock -= cantidad
                    producto.save()  # Guardar los cambios en el producto
                
                    
                    subtotal = producto.precio * cantidad  # Calcular el subtotal del ítem
                    
                    # Sumar al precio total
                    total_precio += subtotal

                    # Guardar los detalles del producto en una lista
                    productos_detalles.append({
                        'nombre_producto': producto.nombre,
                        'cantidad': cantidad,
                        'subtotal': subtotal,
                        'precio_unitario': producto.precio
                    })
                    
                except Exception as e:
                    self.agregar_mensaje(request, "error",  f'Errores al realizar la compra: {e}')  # Manejar errores individuales

            fecha_creacion = "Hoy es x"
            # Escribir los detalles de la compra en un archivo de texto
            
            #realizo esto para prácticar archivos pero esta factura debe guardarse en la base de datos para produccion
            
            with open('venta.txt', 'w', encoding='utf-8') as file:
                file.write('Nombre Producto | Cantidad | Precio Unitario | Subtotal\n')
                file.write('-----------------------------------------------------------\n')
                for producto in productos_detalles:
                    file.write(f"{producto['nombre_producto']} | {producto['cantidad']} | ₡{producto['precio_unitario']} | ₡{producto['subtotal']}\n")
                    
                
                file.write('-----------------------------------------------------\n')
                file.write(f'-----------------  FACTURA  ecomycr  ---------------\n')
                
                file.write('-----------------------------------------------------\n')
                
                file.write(f"Fecha:  {fecha_creacion}---- Total: {total_precio:.2f}.  ")
                
                file.write('-------------------------------------------------------\n')
                
                file.write('--------------------------------------------------------\n')
                
                file.write('-----------------------------------------------------------\n')
            # Mensajes de éxito y confirmación
            self.agregar_mensaje(request,"success", 'Detalles de la compra guardados correctamente en venta.txt.')
            self.agregar_mensaje(request, "success",f'Se realizó la compra de {len(items)} productos.')
            
            messages.info(request, f'Total de la venta: {total_precio:.2f} .')
      
            # Vaciar el carrito después de la compra
            carrito.items.all().delete()
            carrito.delete()

        except Exception as e:
            self.agregar_mensaje(request, "error",  f'Ocurrió un error al realizar la compra: {str(e)}')  # Manejo general de errores

        # Redirigir a la vista del carrito al finalizar el proceso de compra
        return redirect(reverse('carrito'))



