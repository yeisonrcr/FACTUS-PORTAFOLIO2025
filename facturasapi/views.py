from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Cliente, Facturax, DetalleFactura
from .forms import ClienteForm, FacturaForm, DetalleFacturaForm
from .factus_client import FactusClient
import logging

logger = logging.getLogger(__name__)

@require_http_methods(["GET"])
def lista_facturas(request):
    """Display list of all invoices"""
    facturas = Facturax.objects.all().order_by('-created_at')
    
    
    return render(request, 'facturasapi/lista_facturas.html', {'facturas': facturas})

@require_http_methods(["GET", "POST"])
def crear_factura(request):
    """Create new invoice with client and detail information"""
    if request.method == 'POST':
        factura_form = FacturaForm(request.POST)
        cliente_form = ClienteForm(request.POST)
        detalle_form = DetalleFacturaForm(request.POST)

        if all([factura_form.is_valid(), cliente_form.is_valid(), detalle_form.is_valid()]):
            try:
                # Save client information
                cliente = cliente_form.save()
                
                # Save invoice
                factura = factura_form.save(commit=False)
                factura.cliente = cliente
                factura.save()
                
                # Save invoice details
                detalle = detalle_form.save(commit=False)
                detalle.factura = factura
                detalle.save()

                # Create invoice in Factus API
                factus_client = FactusClient()
                payload = prepare_factura_payload(factura, detalle)
                response = factus_client.crear_factura(payload)
                
                # Update local invoice with API response
                factura.respuesta_dian = response
                factura.save()

                messages.success(request, 'Factura creada exitosamente.')
                return redirect('lista_facturas')
            except Exception as e:
                logger.error(f"Error creating invoice: {str(e)}")
                messages.error(request, f'Error al crear la factura: {str(e)}')
    else:
        factura_form = FacturaForm()
        cliente_form = ClienteForm()
        detalle_form = DetalleFacturaForm()

    context = {
        'factura_form': factura_form,
        'cliente_form': cliente_form,
        'detalle_form': detalle_form,
    }
    return render(request, 'facturasapi/crear_factura.html', context)

@require_http_methods(["POST"])
def validar_factura(request, factura_id):
    """Validate invoice with DIAN through Factus API"""
    factura = get_object_or_404(Facturax, id=factura_id)
    try:
        factus_client = FactusClient()
        response = factus_client.validar_factura(factura.numero_factura)
        
        # Update invoice status based on validation response
        factura.estado = 'VALIDADA' if response.get('status') == 'success' else 'ERROR'
        factura.respuesta_dian = response
        factura.save()

        messages.success(request, 'Factura validada exitosamente.')
    except Exception as e:
        logger.error(f"Error validating invoice: {str(e)}")
        messages.error(request, f'Error al validar la factura: {str(e)}')
    
    return redirect('lista_facturas')

def prepare_factura_payload(factura, detalle):
    """Prepare invoice payload for Factus API"""
    return {
        'numero_factura': factura.numero_factura,
        'cliente': {
            'nit': factura.cliente.nit,
            'razon_social': factura.cliente.razon_social,
            'direccion': factura.cliente.direccion,
            'email': factura.cliente.email,
            'telefono': factura.cliente.telefono,
        },
        'detalle': {
            'descripcion': detalle.descripcion,
            'cantidad': float(detalle.cantidad),
            'valor_unitario': float(detalle.valor_unitario),
            'valor_total': float(detalle.valor_total),
        },
        'valor_total': float(factura.valor_total),
    }