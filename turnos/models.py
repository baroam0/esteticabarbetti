
from django.db import models
from django.contrib.auth.models import User

from cosmiatras.models import Cosmetologa
from tratamientos.models import Tratamiento


class Turno(models.Model):
    MODO_PAGO_CHOICES = [
        ('EF', 'Efectivo'),
        ('TR', 'Transferencia'),
        ('TC', 'Tarjeta de crédito'),
        ('OT', 'Otro'),
    ]

    fecha_hora = models.DateTimeField()
    modo_pago = models.CharField(max_length=2, choices=MODO_PAGO_CHOICES)
    comprobante = models.FileField(upload_to='comprobantes/', blank=True, null=True)
    cosmetologa = models.ForeignKey(Cosmetologa, on_delete=models.CASCADE, related_name='turnos')
    tratamientos = models.ManyToManyField(Tratamiento, related_name='turnos')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='turnos')
    fecha_modificacion = models.DateTimeField(auto_now=True)
    observaciones = models.CharField(max_length=500, null=True, blank=True)
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cosmetologa} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"
    
    class Meta:
        verbose_name_plural = "Turnos"


# Create your models here.
