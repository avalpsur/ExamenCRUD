from django.shortcuts import render, redirect
from django.db.models import Q,Prefetch,Avg
from django.forms import modelform_factory
from datetime import timedelta
from .models import *
from .forms import *
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'index.html')

#Lista de promociones
def listar_promociones(request):
    promociones = (Promocion.objects.prefetch_related("productos","usuarios")).all()
    return render(request, 'promocion/lista.html',{"promociones":promociones})


def promocion_create(request):
    
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    
    #formulario = promocionForm(datosFormulario)
    formulario = PromocionForm(datosFormulario)
    
    
    if (request.method == "POST"):
        
        promocion_creada = crear_promocion_generico(formulario)
        if(promocion_creada):
             messages.success(request, 'Se ha creado el promocion '+formulario.cleaned_data.get('nombre')+" correctamente")
             return redirect("promocion_lista")
        
    return render(request, 'promocion/create.html',{"formulario":formulario})


def crear_promocion_generico(formulario):
    promocion_creada = False
    if formulario.is_valid():
        
        promocion = Promocion.objects.create(
                nombre = formulario.cleaned_data.get('nombre'),
                descripcion = formulario.cleaned_data.get('descripcion'),
                descuento = formulario.cleaned_data.get('descuento'),
                fechaPromocion = formulario.cleaned_data.get('fechaPromocion'),
                fechaFinPromocion = formulario.cleaned_data.get('fechaFinPromocion'),
                esta_activa = formulario.cleaned_data.get('esta_activa'),
        )
        
        promocion.productos.set(formulario.cleaned_data.get('productos'))
        promocion.usuarios.set(formulario.cleaned_data.get('usuarios'))

        try:
            promocion.save()
            promocion_creada = True
        except Exception as error:
            print(error)
    return promocion_creada

def promocion_editar(request, promocion_id):
    promocion = Promocion.objects.filter(id=promocion_id).first() 
    
    if request.method == "POST":
        formulario = PromocionForm(request.POST)  
        
        if formulario.is_valid():
            nombre = formulario.cleaned_data.get('nombre'),
            descripcion = formulario.cleaned_data.get('descripcion'),
            descuento = formulario.cleaned_data.get('descuento'),
            fechaPromocion = formulario.cleaned_data.get('fechaPromocion'),
            fechaFinPromocion = formulario.cleaned_data.get('fechaFinPromocion'),
            esta_activa = formulario.cleaned_data.get('esta_activa'),
            promocion.save()  
            
            messages.success(request, f'Se ha editado la promocion "{promocion.nombre}" correctamente')
            return redirect('lista_promociones') 
        
    else:
        formulario = PromocionForm(initial={
            'nombre': promocion.nombre,
            'descripcion': promocion.descripcion,
            'descuento': promocion.descuento,
            'fechaPromocion': promocion.fechaPromocion,
            'fechaFinPromocion': promocion.fechaFinPromocion,
        })
    
    return render(request, 'promocion/actualizar.html', {"formulario": formulario, "promocion": promocion})


def promocion_eliminar(request,promocion_id):
    promocion = Promocion.objects.filter(id=promocion_id).first()
    try:
        promocion.delete()
        messages.success(request, "Se ha elimnado el promocion "+promocion.nombre+" correctamente")
    except Exception as error:
        print(error)
    return redirect('lista_promociones')