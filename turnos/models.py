



from django.db import models

class Turno(models.Model):
    nombre_usuario = models.CharField(max_length=100)
    fecha_turno = models.DateField()
    hora_turno = models.TimeField()
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Turno de {self.nombre_usuario} para el {self.fecha_turno} a las {self.hora_turno}'



# Create your models here.
