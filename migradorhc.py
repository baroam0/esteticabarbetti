
from datetime import datetime
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
    with open(archivo_txt, "r", encoding="latin-1") as f:
        #next(f)
        for linea in f:

            try:
                datos = linea.strip().split(";")
                paciente = Paciente.objects.get(idaccess=datos[1])
                fecha = datos[2].split(" ")
                fechahora = fecha[0] + " " + datos[3]

                fecha_obj = datetime.strptime(fechahora, "%d/%m/%Y %H:%M")

                fecha_formateada = fecha_obj.strftime("%Y-%m-%d %H:%M:%S")

                diagnostico = datos[5].replace("\n", "")
                tratamiento = datos[6].replace("\n", "")

                HistoriaClinica.objects.create(
                    paciente = paciente,
                    idaccess = datos[1],
                    fecha = fecha_formateada,
                    historia = datos[4],
                    diagnostico = diagnostico,
                    tratamiento = tratamiento,
                    primeravez = False,
                    responsable = None
                )

            except Exception as e:
                print(datos)
                print("Error")
                print(str(e))
                break

            #print(f"Paciente {datos[0]} insertado correctamente.")
        
if __name__ == "__main__":
    cargar_hc("Historias2.txt")
