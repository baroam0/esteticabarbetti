
import datetime
import time
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "esteticabarbetti.settings")
django.setup()

from pacientes.models import Paciente
from historiasclinicas.models import HistoriaClinica

def limpiar(valor):
    if valor is None:
        return None
    valor = valor.strip()
    return valor if valor != "" else None


def cargar_hc(archivo_txt):
    inicio = time.time()
    hcs = []
    c = 0
    with open(archivo_txt, "r", encoding="latin-1") as f:
        
        for linea in f:

            datos = linea.strip().split(";")
            print(datos)

            paciente = Paciente.objects.get(
                idaccess=datos[1]
            )

            fechahora = datos[2] + " " + datos[3]
            fecha_obj = datetime.datetime.strptime(fechahora, "%d/%m/%Y %H:%M")
            
            hc = HistoriaClinica(
                    paciente = paciente,
                    idaccess = datos[0],
                    fecha = fecha_obj,
                    historia = datos[4],
                    diagnostico = datos[6],
                    tratamiento = datos[7],
                    primeravez = False,
                    responsable = None
            )
            hcs.append(hc)                
            c = c + 1
                    
    HistoriaClinica.objects.bulk_create(hcs)
            
    fin = time.time()
    diferencia = fin - inicio
    print("Tiempo de ejecucion " + str(diferencia))
    print("Insertadas " + str(c))

if __name__ == "__main__":
    cargar_hc("Historias.txt")
