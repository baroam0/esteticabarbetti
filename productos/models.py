
from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model() 

class Producto(models.Model):
    descripcion = models.TextField(blank=False, null=False, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


class HistorialProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='historial')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)

    precio_registrado = models.DecimalField(max_digits=20, decimal_places=2)
    stock_registrado = models.IntegerField()
    
    accion = models.CharField(max_length=10, choices=[('CREADO', 'Creado'), ('EDITADO', 'Editado')])

    def __str__(self):
        return f'{self.accion} {self.producto.descripcion} por {self.usuario.username if self.usuario else "Sistema"} el {self.fecha_modificacion.strftime("%Y-%m-%d %H:%M")}'

    class Meta:
        verbose_name = "Historial de Producto"
        verbose_name_plural = "Historial de Productos"
        ordering = ['-fecha_modificacion']

# Create your models here.
