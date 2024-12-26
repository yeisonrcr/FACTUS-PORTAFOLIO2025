from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import re
from django.shortcuts import render
from .models import Request

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'vehicle/index.html')

#for showing signup/login button for ADMIN(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('login')

def afterlogin_view(request):
    return redirect('admin-dashboard')



def login_gyna(request):
    return render (request, 'vehicle/adminlogin.html')

#============================================================================================
# ADMIN RELATED views start
#============================================================================================

@login_required(login_url='login')
def admin_dashboard_view(request):
    
    try:
        enquiries = models.Request.objects.all().order_by('-id')  # Cambio de "enquiry" a "enquiries"
    except models.Request.DoesNotExist:
        enquiries = []  # Si no hay solicitudes, crea una lista vacía

    return render(request, 'vehicle/admin_dashboard.html', {'data': enquiries})



@login_required(login_url='login')
def admin_request_view(request):
    return render(request,'vehicle/admin_request.html')





#============================================================================================
# PENDIENTES
#============================================================================================

def paginate_queryset(request, queryset, per_page=10): 
    paginator = Paginator(queryset, per_page) 
    page = request.GET.get('page', 1)
    
    try: 
        paged_data = paginator.page(page) 
    except PageNotAnInteger: 
        paged_data = paginator.page(1) 
    except EmptyPage: 
        paged_data = paginator.page(paginator.num_pages) 
    
    return paged_data



@login_required(login_url='login')
def admin_view_request_view(request):
    try:
        enquiries = models.Request.objects.all().order_by('-id')
    except models.Request.DoesNotExist:
        enquiries = []
    
    paged_data = paginate_queryset(request, enquiries, per_page=10)
    return render(request, 'vehicle/admin_view_request.html', {'data': paged_data})





@login_required(login_url='login')
def admin_pendientes_clientes(request):
    try:
        # Filtrar solicitudes pendientes de envío o cotizadas, ordenadas por ID descendente
        enquiries = models.Request.objects.filter(Q(status='Pendiente de enviar') | Q(estado='Cotizado')).order_by('-id')
    except models.Request.DoesNotExist:
        # Si no hay solicitudes, crea una lista vacía
        enquiries = []
    
    
    paged_data = paginate_queryset(request, enquiries, per_page=10)
    
    return render(request, 'vehicle/admin_pendientes_clientes.html', {'data': enquiries})

@login_required(login_url='login')
def admin_pendientes_dinero(request):
    try:
        enquiries = models.Request.objects.filter(estado='Abonado').order_by('-id')
        
            # Cambio de "enquiry" a "enquiries"
    except models.Request.DoesNotExist:
        enquiries = []  # Si no hay solicitudes, crea una lista vacía
    
    
    paged_data = paginate_queryset(request, enquiries, per_page=10)
    

    return render(request, 'vehicle/admin_pendientes_dinero.html', {'data': enquiries})

@login_required(login_url='login')
def admin_pendientes_distribuidoras(request):
    try:
        enquiries = models.Request.objects.filter(dinomoDis='No buscado').order_by('-id')
        
    except models.Request.DoesNotExist:
        enquiries = []  # Si no hay solicitudes, crea una lista vacía
    
    
    paged_data = paginate_queryset(request, enquiries, per_page=10)

    return render(request, 'vehicle/admin_pendientes_distribuidoras.html', {'data': enquiries})




@login_required(login_url='login')
def admin_pendientes_investigar(request):

    try:
        # Filtrar solicitudes pendientes de envío o cotizadas, ordenadas por ID descendente
        enquiries = models.Request.objects.filter(Q(status='Pendiente de investigar') | Q(dinomoDis='Investigar')).order_by('-id')
    except models.Request.DoesNotExist:
        # Si no hay solicitudes, crea una lista vacía
        enquiries = []
        
        
    return render(request, 'vehicle/admin_pendiente_investigar.html', {'data': enquiries})

@login_required(login_url='login')
def admin_pendientes_distribuidoras_pagados(request):
    try:
        enquiries = models.Request.objects.filter(dinomoDis='Solicitado pero pendiente de enviarmelo').order_by('-id')
        
    except models.Request.DoesNotExist:
        enquiries = []  # Si no hay solicitudes, crea una lista vacía

    return render(request, 'vehicle/admin_pendientes_distribuidoras_pagados.html', {'data': enquiries})

@login_required(login_url='login')
def admin_pendientes_internet(request):

    try:
        # Filtrar solicitudes pendientes de envío o cotizadas, ordenadas por ID descendente
        enquiries = models.Request.objects.filter(Q(tipo__icontains='internet') | Q(distribuidorax__icontains='internet')).order_by('-id')
        
    except models.Request.DoesNotExist:
        # Si no hay solicitudes, crea una lista vacía
        enquiries = []
        
    return render(request, 'vehicle/admin_pendiente_internet.html', {'data': enquiries})

@login_required(login_url='login')
def admin_pendientes_usa(request):
    try:
        enquiries = models.Request.objects.filter(Q(tipo__icontains='Estados Unidos') | Q(distribuidorax__icontains='Estados Unidos')).order_by('-id')
        
    except models.Request.DoesNotExist:
        enquiries = []  # Si no hay solicitudes, crea una lista vacía

    return render(request, 'vehicle/admin_pendientes_usa.html', {'data': enquiries})


@login_required(login_url='login')
def admin_pendientes_panama(request):
    try:
        enquiries = models.Request.objects.filter(Q(tipo__icontains='panama') | Q(distribuidorax__icontains='panama')).extra(where=["LOWER(tipo) LIKE %s"], params=['%panama%']).order_by('-id')
        
        
    except models.Request.DoesNotExist:
        enquiries = []  # Si no hay solicitudes, crea una lista vacía

    return render(request, 'vehicle/admin_pendiente_panama.html', {'data': enquiries})




@login_required(login_url='login')
def admin_pendientes_otros(request):

    try:
        # Filtrar solicitudes pendientes de envío o cotizadas, ordenadas por ID descendente
        
        enquiries = models.Request.objects.filter(Q(tipo__icontains='Otro') | Q(distribuidorax__icontains='Otro')).order_by('-id')
        
        
    except models.Request.DoesNotExist:
        # Si no hay solicitudes, crea una lista vacía
        enquiries = []
        
    return render(request, 'vehicle/admin_pendiente_otros.html', {'data': enquiries})



#============================================================================================
# CAMBIAR DISTRIBUIDORA Y ESTADOS
#============================================================================================


@login_required(login_url='login')
def change_status_view_uno(request,pk):
    adminenquiry=forms.AdminApproveRequestForm()
    if request.method=='POST':
        adminenquiry=forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            
            enquiry_x.costAbonado=adminenquiry.cleaned_data['costAbonado']
            
            enquiry_x.status=adminenquiry.cleaned_data['status']
            
            enquiry_x.estado=adminenquiry.cleaned_data['estado']
            
            enquiry_x.dinomoDis=adminenquiry.cleaned_data['dinomoDis']
            
            
            
            
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-request')
    return render(request,'vehicle/admin_approve_request_details.html',{'adminenquiry':adminenquiry})

@login_required(login_url='login')
def change_status_view_dos(request, pk):
    request_instance = get_object_or_404(Request, id=pk)

    if request.method == 'POST':
        new_distribuidorax = request.POST.get('distribuidorax')
        request_instance.distribuidorax = new_distribuidorax
        request_instance.save()
        return redirect('admin-view-request')  # Redirige a la página adecuada

    return render(request, 'vehicle/admin_approve_request_detailsdos.html', {'request_instance': request_instance})

@login_required(login_url='login')
def change_status_view_tres(request, pk):
    request_instance = get_object_or_404(Request, id=pk)
    
    if request.method == 'POST':
        adminenquiry = forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x = models.Request.objects.get(id=pk)
            
            # Actualiza los campos con los datos del formulario
            enquiry_x.costAbonado = adminenquiry.cleaned_data['costAbonado']
            enquiry_x.status = adminenquiry.cleaned_data['status']
            enquiry_x.estado = adminenquiry.cleaned_data['estado']
            enquiry_x.dinomoDis = adminenquiry.cleaned_data['dinomoDis']
            enquiry_x.save()
        else:
            print("El formulario no es válido")
        return HttpResponseRedirect('/admin-view-request')  # Asegúrate de proporcionar la URL correcta
    else:
        adminenquiry = forms.AdminApproveRequestForm()
        return render(request, 'vehicle/admin_approve_request_details.html', {'adminenquiry': adminenquiry, 'request_instance': request_instance})



#============================================================================================
# AGREGAR CONSULTA ADMIN
#============================================================================================

@login_required(login_url='login')
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
            estado_seleccionado = request.POST.get('estado')
            dinomoDis_seleccionado = request.POST.get('dinomoDis')
            
            # Asigna el estado seleccionado a la instancia de 'enquiry'
            
            enquiry.instance.status = status_seleccionado
            enquiry.instance.estado = estado_seleccionado
            
            enquiry.instance.dinomoDis =dinomoDis_seleccionado
            enquiry.save()
            
            return HttpResponseRedirect('admin-view-request')  # Asegúrate de proporcionar la URL correcta
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




@login_required(login_url='login')
def admin_cliente_busqueda(request):
    pass
    '''
    datos = request.GET.get('datosclientebusqueda')
    datos = re.sub(r'\s|-', '', datos)  # Elimino espacios y guiones
    print("Este es el dato buscado: " + str(datos))
    
    # Buscar clientes por dirección o teléfono
    datas = models.Customer.objects.filter(Q(address__icontains=datos) | Q(mobile__icontains=datos)).order_by('id')
    try:  
        if datas:

            
            return render(request, 'vehicle/admin_cliente_busqueda.html', {'customers': datas})
        else:
            print("No se ha encontrado nada con eso")
            return render(request, 'vehicle/admin_cliente_busqueda.html', {'customers': datas})
    except:
        pass
        
@login_required(login_url='login')
def admin_busqueda(request):
    if request.method == 'GET':
        datos = request.GET.get('datosbusqueda')
        datos = re.sub(r'\s|-', '', datos)
        datas = models.Request.objects.filter(Q(vehicle_cliente__icontains=datos) | Q(vehicle_mobile__icontains=datos) |
Q(vehicle_brand__icontains=datos)).order_by('id')
        if datas:
            return render(request, 'vehicle/admin_cliente_busqueda.html',  {'data': datas})
        else:
            print("No se ha encontrado nada con eso")
            
        enquiries = []
        if re.match(r'^\d{8,}$', datos):
            if len(datos)>8:  # Es un VIN
                try:
                    enquiries = models.Request.objects.filter(vehicle_no=datos).order_by('-id')
                    
                    return render(request, 'vehicle/admin_search.html',  {'data': enquiries})
                    
                except models.Request.DoesNotExist:
                    enquiries = []  # No se encontró ningún cliente con ese número de teléfono

        elif re.match(r'^[A-Z0-9a-záéíóúÁÉÍÓÚñÑ\s]+$', datos):
            datos = datos.lower()
            try:
                
                enquiries = models.Request.objects.filter(vehicle_model__iexact=datos).order_by('-id')
            except models.Request.DoesNotExist:
                enquiries = []
            if enquiries:
                print("se ha encontrado datos")
            else:
                try:
                    enquiries = models.Request.objects.filter(vehicle_name__iexact=datos).order_by('-id')
                except models.Request.DoesNotExist:
                    enquiries = []
            if enquiries:
                print("se ha encontrado datos")
            else:
                try:
                    datos= datos.lower()
                    
                    enquiries = models.Request.objects.filter(vehicle_no__iexact=datos).order_by('-id')
                    
                except models.Request.DoesNotExist:
                    enquiries = []
        return render(request, 'vehicle/admin_search.html',  {'data': enquiries})




        elif re.match(r'^[A-Z0-9a-záéíóúÁÉÍÓÚñÑ\s]+$', datos):
            datos = datos.lower()
            
            try:
                if not enquiries:
                    try:
                        datos = datos.lower()
                        enquiries = models.Request.objects.filter(vehicle_no__iexact=datos).order_by('-id')
                    except models.Request.DoesNotExist:
                        enquiries = []
                    
                
            except models.Request.DoesNotExist:
                enquiries = []



            if re.match(r'^\d{10,}+$', datos):
                if len(datos) > 10:  # Es un VIN
                    try:
                        enquiries = models.Request.objects.filter(vehicle_no=datos).order_by('-id')
                        return render(request, 'vehicle/admin_search.html', {'data': enquiries})
                    except models.Request.DoesNotExist:
                        enquiries = []  # No se encontró ningún cliente con ese número de teléfono
            

'''


@login_required(login_url='login')
def admin_busqueda(request):
    if request.method == 'GET':
        datos = request.GET.get('datosbusqueda')
        datos = re.sub(r'\s|-', '', datos)
        datas = models.Request.objects.filter(
            Q(vehicle_cliente__icontains=datos) |
            Q(vehicle_mobile__icontains=datos) |
            Q(vehicle_model__icontains=datos) |
            Q(vehicle_name__icontains=datos) |
            Q(vehicle_brand__icontains=datos)
        ).order_by('id')

        if datas:
            return render(request, 'vehicle/admin_cliente_busqueda.html', {'data': datas})
        else:

            enquiries = []
            
            if re.match(r'^[A-Z0-9a-záéíóúÁÉÍÓÚñÑ\s]+$', datos):
                datos = datos.lower()
                
                try:
                    if not enquiries:
                        try:
                            datos = datos.lower()
                            enquiries = models.Request.objects.filter(vehicle_no__iexact=datos).order_by('-id')
                        except models.Request.DoesNotExist:
                            enquiries = []
                        
                    
                except models.Request.DoesNotExist:
                    enquiries = []
                
                
        
                

        return render(request, 'vehicle/admin_search.html', {'data': enquiries})



@login_required(login_url='login')
def admin_customer_view(request):
    return render(request,'vehicle/admin_customer.html')



def error_404(request, exception):
    context = {}
    return render(request,'404.html', context)









