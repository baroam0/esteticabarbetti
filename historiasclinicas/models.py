

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

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

    def save(self, *args, **kwargs):
        # Si la fecha está vacía o nula, asignamos la fecha y hora actual
        if not self.fecha:
            self.fecha = timezone.now()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Historias Clinicas"

class ImagenHistoriaClinica(models.Model):
    historiaclinica = models.ForeignKey(
        'HistoriaClinica',
        on_delete=models.CASCADE,
        related_name='imagenes'
    )
    imagen = models.ImageField(upload_to='historias_clinicas/')

    def __str__(self):
        return f"Imagen de {self.historiaclinica.diagnostico}"


# Create your models here.
