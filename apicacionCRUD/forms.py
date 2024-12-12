from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime



class PromocionForm(forms.Form):
    
    nombre = forms.CharField(label="Nombre de la promoción",
                             required=True, 
                            )
    
    
    descripcion = forms.CharField(label="Descripción",
                                  required=False,
                                  min_length=100,
                                  widget=forms.Textarea())
    
    productosDisponibles = Producto.objects.all()
    productos = forms.ModelMultipleChoiceField(
        queryset= productosDisponibles,
        required=True,
        help_text="Mantén pulsada la tecla control para seleccionar varios elementos"
    )
    
    usuariosDisponibles = Usuario.objects.all()
    usuarios = forms.ModelMultipleChoiceField(
        queryset= usuariosDisponibles,
        required=True,
        help_text="Mantén pulsada la tecla control para seleccionar varios elementos"
    )
    
    descuento = forms.IntegerField(label="Descuento",
                                   required=True)
    
    fechaPromocion = forms.DateField(label="Fecha de inicio de la promoción",
                                        initial=datetime.date.today,
                                        widget= forms.SelectDateWidget()
                                        )
    
    fechaFinPromocion = forms.DateField(label="Fecha del fin de la promoción",
                                        initial=datetime.date.today,
                                        widget= forms.SelectDateWidget()
                                        )
    esta_activa = forms.BooleanField(label="Está activa",
                                     )
    
    def clean(self):
        
        super().clean()
        
        nombre = self.cleaned_data.get('nombre'),
        descripcion = self.cleaned_data.get('descripcion'),
        descuento = self.cleaned_data.get('descuento'),
        productos = self.cleaned_data.get('productos'),
        usuarios = self.cleaned_data.get('usuarios'),
        fechaPromocion = self.cleaned_data.get('fechaPromocion'),
        fechaFinPromocion = self.cleaned_data.get('fechaFinPromocion'),
        esta_activa = self.cleaned_data.get('esta_activa'),
        
        promocionNombre = Promocion.objects.prefetch_related("productos","usuarios").filter(nombre=nombre).first()
        if not promocionNombre is None:
             self.add_error('nombre','Ya existe una promoción con ese nombre')
             
        if len(descripcion) < 100:
            self.add_error('descripcion','Al menos debes indicar 3 caracteres')

        
        if productos.puede_tener_promociones == False:
            self.add_error('productos','A este producto no se le pueden aplicar promociones')
            
        if usuarios.edad < 18 :
            self.add_error('usuarios','El usuario debe ser mayor de edad')
            
        if descuento < 0 or descuento > 10:
            self.add_error('descuento','El descuento tiene que ser entre el 0 y el 10%')
            
        if fechaPromocion > fechaFinPromocion:
             self.add_error('fechaPromocion','La fecha de inicio de la promoción debe ser mayor a la del fin')
        
        return self.cleaned_data