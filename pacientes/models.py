
from datetime import date
from django.db import models


class Paciente(models.Model):
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('I', 'Indefinido'),
    )
    
    idaccess=models.IntegerField(blank=True, null=True)
    nombre=models.CharField(null=False, blank=False, max_length=500)
    fechanacimiento=models.DateField(null=True, blank=True)

    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES,
        default='M'
    )

    estadocivil=models.CharField(null=True, blank=True, max_length=50)
    numerodocumento=models.CharField(null=True, blank=True, max_length=20)
    domicilio=models.CharField(null=True, blank=True, max_length=500)
    correoelectronico=models.EmailField(null=True,blank=True)
    obrasocial=models.CharField(null=True, blank=True, max_length=500)
    telefono=models.CharField(null=True, blank=True, max_length=50)
    notas=models.CharField(null=True, blank=True, max_length=500)
    proximoturno=models.CharField(null=True, blank=True, max_length=500)

    foto = models.ImageField(
        upload_to='fotos/',
        null=True,
        blank=True
    )
    aviso=models.CharField(null=True, blank=True, max_length=500)
    
    def __str__(self):
        return self.nombre.upper()

    def edad(self):
        if self.fechanacimiento:
            hoy = date.today()
            return (
                hoy.year - self.fechanacimiento.year
                - ((hoy.month, hoy.day) < (self.fechanacimiento.month, self.fechanacimiento.day))
            )
        return None
    
    class Meta:
        verbose_name_plural = "Pacientes"


# Create your models here.
