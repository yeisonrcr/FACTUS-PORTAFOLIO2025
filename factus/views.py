from django.shortcuts import render, redirect
from .models import Item
from .forms import FacturaForm, BillingPeriodForm, CustomerForm


from django.contrib.auth.decorators import login_required
from django.db import transaction  # Importar el módulo de transacciones de Django

# Función para crear una factura
@login_required  # Decorador para asegurar que solo los usuarios autenticados pueden acceder
def create_factura(request):
    # Obtener los ítems del carrito y el usuario desde la sesión
    cart_items = request.session.get('cart_items', [])  # Obtener los ítems del carrito desde la sesión
    user = request.user  # Obtener el usuario actual

    # Verificar si el método de la solicitud es POST
    if request.method == 'POST':
        factura_form = FacturaForm(request.POST)  # Crear una instancia de FacturaForm con los datos POST
        billing_period_form = BillingPeriodForm(request.POST)  # Crear una instancia de BillingPeriodForm con los datos POST
        customer_form = CustomerForm(request.POST)  # Crear una instancia de CustomerForm con los datos POST
        
        # Verificar si todos los formularios son válidos
        if (factura_form.is_valid() and billing_period_form.is_valid() and 
            customer_form.is_valid()):
            
            try:
                with transaction.atomic():  # Usar una transacción atómica para asegurar la integridad de los datos
                    # Guardar el periodo de facturación y el cliente
                    billing_period = billing_period_form.save()  # Guardar el periodo de facturación
                    customer = customer_form.save()  # Guardar el cliente
                    
                    # Crear y guardar la factura sin comprometer inmediatamente con la base de datos
                    factura = factura_form.save(commit=False)  
                    factura.billing_period = billing_period  # Asignar el periodo de facturación a la factura
                    factura.customer = customer  # Asignar el cliente a la factura
                    factura.save()  # Guardar la factura
                    
                    # Agregar ítems a la factura
                    for item_data in cart_items:
                        item = Item.objects.create(
                            code_reference=item_data['code_reference'],
                            name=item_data['name'],
                            quantity=item_data['quantity'],
                            price=item_data['price']
                        )  # Crear una instancia del ítem y guardarlo en la base de datos
                        factura.items.add(item)  # Añadir el ítem a la factura
                    
                    # Guardar la factura nuevamente después de agregar los ítems
                    factura.save()
                
                print("se ha creado una factura correctamente")  # Imprimir mensaje de éxito en la consola
                return redirect('lista_repuestos')  # Redirigir a la página principal

            except Exception as e:  # Capturar cualquier excepción que ocurra
                # Manejo de errores
                messages.error(request, f'Error al procesar la factura: {e}')  # Mostrar mensaje de error
        
    else:
        # Si la solicitud no es POST, crear instancias vacías de los formularios
        factura_form = FacturaForm()  # Crear una instancia vacía de FacturaForm
        billing_period_form = BillingPeriodForm()  # Crear una instancia vacía de BillingPeriodForm
        customer_form = CustomerForm()  # Crear una instancia vacía de CustomerForm
        
    # Renderizar el template de creación de factura con los formularios y otros datos necesarios
    return render(request, 'factus/create_factura.html', {
        'factura_form': factura_form,
        'billing_period_form': billing_period_form,
        'customer_form': customer_form,
        'cart_items': cart_items,
        'user': user
    })  # Renderizar la plantilla 'create_factura.html' con los formularios y datos necesarios
