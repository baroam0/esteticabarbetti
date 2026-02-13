

from django.contrib.auth.models import User
from django.db import models


class Ingreso(models.Model):
    fecha = models.DateField(blank=False, null=False)
    descripcion = models.TextField(
        max_length=500, null=False, blank=False
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    TURNO_CHOICES = (
        ('M', 'Mañana'),
        ('T', 'Tarde')
    )

    turno = models.CharField(
        max_length=1,
        choices=TURNO_CHOICES,
        default='M',null=True
    )

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"


# Create your models here.
