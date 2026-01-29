import os
import django
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "esteticabarbetti.settings")
django.setup()

from pacientes.models import Paciente

RUTA_ARCHIVO = "Identificacion.txt" 

def cargar_pacientes():
    cant = 0
    with open(RUTA_ARCHIVO, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            sss = linea.split(";")
            nombre = sss[1]
            if sss[2]:
                fechat = sss[2].replace(" ", "")
                fecha = datetime.strptime(fechat, "%d/%m/%Y").date()
            else:
                fecha=None
            domicilio = sss[6]
            telefono = sss[9]
            
            existe = Paciente.objects.filter(
                idaccess=sss[0]
            ).exists()

            if existe:
                #print(f"Ya existe: {nombre} - {fecha}")
                continue
            else:
                Paciente.objects.create(
                    idaccess=sss[0],
                    nombre=nombre,
                    fechanacimiento=fecha,
                    domicilio=domicilio,
                    telefono=telefono
                )
                cant = cant + 1
                #print(f"Insertado: {nombre} - {fecha}")
    print("Total: " + str(cant))

if __name__ == "__main__":
    cargar_pacientes()
