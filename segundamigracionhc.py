import os
import django

from datetime import datetime

from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "esteticabarbetti.settings")
django.setup()

from pacientes.models import Paciente
from historiasclinicas.models import HistoriaClinica

RUTA_ARCHIVO = "Historias.txt" 

def cargar_hc():
    cant = 0
    with open(RUTA_ARCHIVO, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue

            sss = linea.split(";")

            fecha = sss[2] + " " + sss[3]
            fecha_obj = datetime.strptime(fecha, "%d/%m/%Y %H:%M")
            
            existe = HistoriaClinica.objects.filter(
                fecha=fecha_obj
            ).exists()

            if existe:
                continue
            else:
                paciente = Paciente.objects.get(idaccess=sss[1])

                fecha = sss[2] + " " + sss[3]
                #fecha_obj = datetime.strptime(fecha, "%d/%m/%Y %H:%M")

                fecha_obj = timezone.make_aware(
                    datetime.strptime(fecha, "%d/%m/%Y %H:%M"),
                    timezone.get_current_timezone()
                )

                HistoriaClinica.objects.create(
                    paciente=paciente,
                    idaccess=sss[0],
                    fecha=fecha_obj,
                    historia=sss[4],
                    diagnostico=sss[6], 
                    tratamiento=sss[7],
                    primeravez=False,
                    responsable = None
                )
                cant = cant + 1
                #print(f"Insertado: {paciente.nombre}")
    print("Total: " + str(cant))

if __name__ == "__main__":
    cargar_hc()
