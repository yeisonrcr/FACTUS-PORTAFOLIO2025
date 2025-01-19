
from django.forms import modelformset_factory

from repuestos.forms import RepuestoForm, ImagenRepuestoForm
from repuestos.models import ImagenRepuesto, Repuesto

import re

from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from . import forms,models

from django.contrib.auth.decorators import login_required
from django.db.models import Q

import re
from django.shortcuts import render
from .models import Request
from repuestos.models import Orden
from django.core.paginator import Paginator

from django.urls import reverse
from django.contrib import messages

def editar_consulta(request, id):
    instance = get_object_or_404(Request, id=id)
    if request.method == 'POST':
        form = forms.RequestForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta actualizada exitosamente')
            return redirect(reverse('ver-consultas'))  # Cambia 'your-view-name' por la vista a la que quieres redirigir después de guardar
    else:
        form = forms.RequestForm(instance=instance)
    return render(request, 'vehicle/editar_consulta.html', {'form': form})


@login_required(login_url='casa-admin')
def admin_ver_consultas(request):
    try:
        # Obtener todas las consultas ordenadas por id descendente
        enquiries = models.Request.objects.all().order_by('-id')
        
        # Crear un paginador con 20 items por página (4 columnas × 5 filas)
        paginator = Paginator(enquiries, 6)
        
        # Obtener el número de página de la URL
        page_number = request.GET.get('page')
        
        # Obtener la página específica
        page_obj = paginator.get_page(page_number)
        
    except models.Request.DoesNotExist:
        page_obj = []
    
    return render(request, 'vehicle/ver_consultas.html', {
        'data': page_obj,
        'page_obj': page_obj,
    })




def home_view(request):
    return render(request,'vehicle/index.html')








#for showing signup/login button for ADMIN(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return redirect('login')
    return redirect('casa-admin')



def afterlogin_view(request):
    return redirect('admin-dashboard')



#============================================================================================
# ADMIN RELATED views start
#============================================================================================

def admin_dashboard_view(request):
    return render(request, 'vehicle/admin_dashboard.html')



def admin_request_view(request):
    return render(request,'vehicle/admin_request.html')





#============================================================================================
# PENDIENTES
#============================================================================================




@login_required(login_url='casa-admin')
def admin_view_request_view(request):
    try:
        enquiries = models.Request.objects.all().order_by('-id')
        paginator = Paginator(enquiries, 10)  # Mostrar 10 consultas por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except models.Request.DoesNotExist:
        page_obj = []  # Si no hay solicitudes, crea una lista vacía

    return render(request, 'vehicle/admin_view_request.html', {'page_obj': page_obj})




@login_required(login_url='casa-admin')
def admin_pendientes_clientes(request):
    try:
        enquiries = models.Request.objects.filter(Q(status='Pendiente de enviar') | Q(dinomoDis='Sin estado')).order_by('-id')
    except models.Request.DoesNotExist:
        enquiries = []

    paginator = Paginator(enquiries, 10)  # Muestra 10 solicitudes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vehicle/admin_pendientes_clientes.html', {'page_obj': page_obj})



@login_required(login_url='casa-admin')
def pendientes_pagar(request):
    #consultas pagadas
    try:
        enquiries = models.Request.objects.filter(dinomoDis='Monto pendiente').order_by('-id')
    except models.Request.DoesNotExist:
        enquiries = []

    paginator = Paginator(enquiries, 10)  # Muestra 10 solicitudes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vehicle/monto_pagado.html', {'page_obj': page_obj})


@login_required(login_url='casa-admin')
def admin_pendientes_dinero(request):
    #consultas pagadas
    try:
        enquiries = models.Request.objects.filter(dinomoDis='Monto pagado').order_by('-id')
    except models.Request.DoesNotExist:
        enquiries = []

    paginator = Paginator(enquiries, 10)  # Muestra 10 solicitudes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vehicle/monto_pagado.html', {'page_obj': page_obj})






@login_required(login_url='casa-admin')
def admin_pendientes_distribuidoras(request):
    try:
        enquiries = models.Request.objects.filter(status='Pendiente en llegar').order_by('-id')
    except models.Request.DoesNotExist:
        enquiries = []

    paginator = Paginator(enquiries, 10)  # Muestra 10 solicitudes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vehicle/admin_pendientes_distribuidoras.html', {'page_obj': page_obj})




#pendiente de investigar
@login_required(login_url='casa-admin')
def admin_pendientes_investigar(request):
    try:
        enquiries = models.Request.objects.filter(Q(status='Pendiente de investigar') | Q(dinomoDis='Investigar')).order_by('-id')
    except models.Request.DoesNotExist:
        enquiries = []

    paginator = Paginator(enquiries, 10)  # Muestra 10 solicitudes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vehicle/admin_pendiente_investigar.html', {'page_obj': page_obj})

#solo consultas
@login_required(login_url='casa-admin')
def solo_consultas(request):
    try:
        enquiries = models.Request.objects.filter(Q(status='Consulta') | Q(dinomoDis='Completado')   ).order_by('-id')
    except models.Request.DoesNotExist:
        enquiries = []

    paginator = Paginator(enquiries, 10)  # Muestra 10 solicitudes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vehicle/admin_pendiente_investigar.html', {'page_obj': page_obj})

#solo compras_no_entregadas
@login_required(login_url='casa-admin')
def compras_no_entregadas(request):
    try:
        enquiries = models.Request.objects.filter(Q(status='Pendiente en llegar') | Q(status='Pendiente de enviar') | Q(dinomoDis='Monto pendiente') | Q(dinomoDis='Pendiente') ).order_by('-id')
    except models.Request.DoesNotExist:
        enquiries = []

    paginator = Paginator(enquiries, 10)  # Muestra 10 solicitudes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vehicle/admin_pendiente_investigar.html', {'page_obj': page_obj})


#solo compras_entregadas
@login_required(login_url='casa-admin')
def compras_entregadas(request):
    try:
        enquiries = models.Request.objects.filter(Q(status='Compra entregada')  ).order_by('-id')
    except models.Request.DoesNotExist:
        enquiries = []

    paginator = Paginator(enquiries, 10)  # Muestra 10 solicitudes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vehicle/admin_pendiente_investigar.html', {'page_obj': page_obj})












@login_required(login_url='casa-admin')
def admin_pendientes_distribuidoras_pagados(request):
    try:
        enquiries = models.Request.objects.filter(status='Pendiente en llegar').order_by('-id')
    except models.Request.DoesNotExist:
        enquiries = []

    paginator = Paginator(enquiries, 10)  # Muestra 10 solicitudes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vehicle/admin_pendientes_distribuidoras_pagados.html', {'page_obj': page_obj})




@login_required(login_url='casa-admin')
def admin_pendientes_asia(request):
    try:
    
        enquiries = models.Request.objects.filter( Q(tipo__icontains='asia') | Q(tipo__icontains='Korea') | Q(tipo__icontains='China') | Q(distribuidorax__icontains='Asia') | Q(distribuidorax__icontains='Japon') | Q(distribuidorax__icontains='Korea') ).order_by('-id')
    
    except models.Request.DoesNotExist:
        enquiries = []

    paginator = Paginator(enquiries, 10)  # Muestra 10 solicitudes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vehicle/admin_pendiente_internet.html', {'page_obj': page_obj})


@login_required(login_url='casa-admin')
def admin_pendientes_internet(request):
    try:
        enquiries = models.Request.objects.filter(Q(tipo__icontains='Internet') | Q(distribuidorax__icontains='internet')).order_by('-id')
    except models.Request.DoesNotExist:
        enquiries = []

    paginator = Paginator(enquiries, 10)  # Muestra 10 solicitudes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vehicle/admin_pendiente_internet.html', {'page_obj': page_obj})

@login_required(login_url='casa-admin')
def admin_pendientes_usa(request):
    try:
        enquiries = models.Request.objects.filter(Q(tipo__icontains='Estados Unidos') | Q(distribuidorax__icontains='Estados Unidos')).order_by('-id')
    except models.Request.DoesNotExist:
        enquiries = []

    paginator = Paginator(enquiries, 10)  # Muestra 10 solicitudes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vehicle/admin_pendientes_usa.html', {'page_obj': page_obj})

@login_required(login_url='casa-admin')
def admin_pendientes_panama(request):
    try:
        enquiries = models.Request.objects.filter(Q(tipo__icontains='panama') | Q(distribuidorax__icontains='panama')).extra(where=["LOWER(tipo) LIKE %s"], params=['%panama%']).order_by('-id')
    except models.Request.DoesNotExist:
        enquiries = []

    paginator = Paginator(enquiries, 10)  # Muestra 10 solicitudes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vehicle/admin_pendiente_panama.html', {'page_obj': page_obj})

@login_required(login_url='casa-admin')
def admin_pendientes_otros(request):
    try:
        enquiries = models.Request.objects.filter(Q(tipo__icontains='Otro') | Q(distribuidorax__icontains='Otro')).order_by('-id')
    except models.Request.DoesNotExist:
        enquiries = []

    paginator = Paginator(enquiries, 10)  # Muestra 10 solicitudes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vehicle/admin_pendiente_otros.html', {'page_obj': page_obj})





#============================================================================================
# CAMBIAR DISTRIBUIDORA Y ESTADOS
#============================================================================================


@login_required(login_url='casa-admin')
def change_status_view_uno(request,pk):
    adminenquiry=forms.AdminApproveRequestForm()
    if request.method=='POST':
        adminenquiry=forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            
            enquiry_x.status=adminenquiry.cleaned_data['status']
            
            
            enquiry_x.dinomoDis=adminenquiry.cleaned_data['dinomoDis']
            
            
            
            
            enquiry_x.save()
        else:
            print("form is invalid")
        return redirect('/admin-view-request')
    return render(request,'vehicle/admin_approve_request_details.html',{'adminenquiry':adminenquiry})

@login_required(login_url='casa-admin')
def change_status_view_dos(request, pk):
    request_instance = get_object_or_404(Request, id=pk)

    if request.method == 'POST':
        new_distribuidorax = request.POST.get('distribuidorax')
        request_instance.distribuidorax = new_distribuidorax
        request_instance.save()
        return redirect('admin-view-request')  # Redirige a la página adecuada

    return render(request, 'vehicle/admin_approve_request_detailsdos.html', {'request_instance': request_instance})




@login_required(login_url='casa-admin')
def change_status_view_tres(request, pk):
    request_instance = get_object_or_404(Request, id=pk)
    
    if request.method == 'POST':
        adminenquiry = forms.AdminApproveRequestForm(request.POST, instance=request_instance)
        if adminenquiry.is_valid():
            enquiry_x = models.Request.objects.get(id=pk)
            
            # Actualiza los campos con los datos del formulario
            enquiry_x.save()
        else:
            mensaje = "El formulario no es valido"
        return redirect('admin-view-request')  # Asegúrate de proporcionar la URL correcta
    else:
        adminenquiry = forms.AdminApproveRequestForm(instance=request_instance)
        return render(request, 'vehicle/admin_approve_request_details.html', {'adminenquiry': adminenquiry, 'request_instance': request_instance})


#============================================================================================
# AGREGAR CONSULTA ADMIN
#============================================================================================

@login_required(login_url='casa-admin')
def admin_add_request_view(request):
    enquiry=forms.RequestForm()
    mydict={'enquiry':enquiry}
    
    if request.method == 'POST':
        enquiry = forms.RequestForm(request.POST)
        
        
        if enquiry.is_valid():
            enquiry_x = enquiry.save(commit=False)
            enquiry_x.save()
            
            # Obtén el valor seleccionado del campo 'estado'
            status_seleccionado = request.POST.get('status')
            dinomoDis_seleccionado = request.POST.get('dinomoDis')
            
            # Asigna el estado seleccionado a la instancia de 'enquiry'
            
            enquiry.instance.status = status_seleccionado
            
            enquiry.instance.dinomoDis =dinomoDis_seleccionado
            enquiry.save()
            
            return redirect('admin-view-request')  # Asegúrate de proporcionar la URL correcta
        else:
            print("El formulario no es válido")
            mydict = {'errors': enquiry.errors}
    else:
        enquiry = forms.RequestForm()
        mydict = {'enquiry': enquiry}

    return render(request, 'vehicle/admin_add_request.html', context=mydict)





#============================================================================================
# BUSQUEDA
#============================================================================================




@login_required(login_url='casa-admin')
def admin_cliente_busqueda(request):
    pass

@login_required(login_url='casa-admin')
def admin_busqueda(request):
    if request.method == 'GET':
        datos = request.GET.get('datosbusqueda', '')
        datos = re.sub(r'\s|-', '', datos)  # Normaliza el texto de búsqueda
        
        # Buscar coincidencias en los campos relevantes
        datas = models.Request.objects.filter(
            Q(vehicle_cliente__icontains=datos) |
            Q(vehicle_mobile__icontains=datos) |
            Q(vehicle_model__icontains=datos) |
            Q(vehicle_name__icontains=datos) |
            Q(vehicle_brand__icontains=datos)
        ).order_by('-id')
        
        # Si no hay resultados en `datas`, buscar por `vehicle_no`
        if not datas.exists():
            if re.match(r'^[A-Z0-9a-záéíóúÁÉÍÓÚñÑ\s]+$', datos):
                datas = models.Request.objects.filter(vehicle_no__iexact=datos).order_by('-id')
        
        # Aplicar paginación
        paginator = Paginator(datas, 10)  # Mostrar 10 resultados por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'vehicle/admin_search.html', {'page_obj': page_obj, 'datosbusqueda': datos})






@login_required(login_url='casa-admin')
def admin_customer_view(request):
    return render(request,'vehicle/admin_customer.html')



def error_404(request, exception):
    context = {}
    return render(request,'404.html', context)











@login_required(login_url='casa-admin')
def mostrar_ordenes_tienda(request):
    try:
        enquiries = Orden.objects.all().order_by('-fecha_compra')
    except Orden.DoesNotExist:
        enquiries = []

    paginator = Paginator(enquiries, 10)  # Muestra 10 solicitudes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vehicle/mostrar_ordenes.html', {'page_obj': page_obj})

@login_required(login_url='casa-admin')
def detalle_orden(request, id):
    orden = get_object_or_404(Orden, id=id)
    items_orden = orden.items.all()  # Obtiene todos los items relacionados con la orden

    return render(request, 'vehicle/detalle_orden.html', {'orden': orden, 'items_orden': items_orden})


