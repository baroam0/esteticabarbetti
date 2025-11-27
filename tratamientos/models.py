
from django.contrib.auth.models import User
from django.db import models


class Tratamiento(models.Model):
    descripcion = models.CharField(max_length=50, unique=True)
    precio = models.DecimalField(max_digits=20, decimal_places=2) 
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.descripcion.upper()
    
    def save(self, *args, **kwargs):
        self.descripcion = self.descripcion.upper()
        super(Tratamiento, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Tratamientos"


# Create your models here.
