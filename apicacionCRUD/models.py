from django.db import models
from django.utils import timezone

# Create your models here.
class Usuario(models.Model):    
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    puede_tener_promociones = models.BooleanField()

    def __str__(self):
        return self.nombre

class Promocion(models.Model):
    nombre = models.CharField(unique=True, max_length=100)
    descripcion = models.TextField(max_length=300)
    productos    = models.ManyToManyField(Producto, related_name='promociones_productos')
    usuarios = models.ManyToManyField(Usuario, related_name='promociones_usuarios')
    descuento = models.IntegerField()
    fechaPromocion = models.DateField()
    fechaFinPromocion = models.DateField()
    esta_activa = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre