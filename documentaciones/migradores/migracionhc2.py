from datetime import datetime
import time
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "esteticabarbetti.settings")
django.setup()

from pacientes.models import Paciente
from historiasclinicas.models import HistoriaClinica


def cargar_hc(archivo_txt):
    historias_a_insertar = []  # lista para acumular objetos

    with open(archivo_txt, "r", encoding="latin-1") as f:
        inicio = time.time()
        for linea in f:
            lineacompleta = linea.split("mariana")
            for i, l in enumerate(lineacompleta):
                try:
                    datos = l.strip().split(";")
                    paciente = Paciente.objects.get(idaccess=datos[1])
                    fecha = datos[2].split(" ")
                    fechahora = fecha[0] + " " + datos[3]

                    fecha_obj = datetime.strptime(fechahora, "%d/%m/%Y %H:%M")

                    diagnostico = datos[5].replace("\n", "")
                    tratamiento = datos[6].replace("\n", "")

                    historia = HistoriaClinica(
                        paciente=paciente,
                        idaccess=datos[1],
                        fecha=fecha_obj,  # mejor guardar como datetime directamente
                        historia=datos[4],
                        diagnostico=diagnostico,
                        tratamiento=tratamiento,
                        primeravez=False,
                        responsable=None
                    )
                    historias_a_insertar.append(historia)

                except Exception as e:
                    print(datos)
                    print("Error")
                    print(str(e))
                    break
        fin = time.time()
        diferencia = fin - inicio
        print("Ejecucion en " + str(diferencia))

    # Inserción masiva en una sola operación
    if historias_a_insertar:
        HistoriaClinica.objects.bulk_create(historias_a_insertar)
        print(f"Se insertaron {len(historias_a_insertar)} historias clínicas.")


if __name__ == "__main__":
    cargar_hc("Historias2.txt")
