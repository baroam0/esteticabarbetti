
from django.contrib.auth.models import User
from django.db import models

from pacientes.models import Paciente


class HistoriaClinica(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    idaccess = models.IntegerField(null=True, blank=True)
    fecha = models.DateTimeField()
    historia = models.CharField(max_length=1000, null=True, blank=True)
    diagnostico = models.CharField(max_length=1000, null=True, blank=True)
    tratamiento = models.CharField(max_length=1000, null=True, blank=True)
    primeravez = models.BooleanField(default=False)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.diagnostico
    
    class Meta:
        verbose_name_plural = "Historias Clinicas"

class ImagenHistoriaClinica(models.Model):
    historiaclinica = models.ForeignKey(
        'HistoriaClinica',
        on_delete=models.CASCADE,
        related_name='imagenes'
    )
    imagen = models.ImageField(upload_to='historias_clinicas/')
    descripcion = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Imagen de {self.historia.diagnostico}"


# Create your models here.
