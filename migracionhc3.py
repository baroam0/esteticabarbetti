from datetime import datetime
import time
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "esteticabarbetti.settings")
django.setup()

from django.contrib.auth.models import User
from pacientes.models import Paciente
from historiasclinicas.models import HistoriaClinica



def cargar_hc(archivo_txt):
    historias_a_insertar = []

    usuario = User.objects.get(pk=2)

    with open(archivo_txt, "r", encoding="latin-1") as f:
        inicio = time.time()

        for linea in f:
            if not linea.strip():
                continue

            try:
                # Separar por ;
                datos = [d.strip() for d in linea.split(";")]

                # Estructura esperada:
                # 0: paciente_id
                # 1: idaccess
                # 2: fecha
                # 3: hora
                # 4: historia (texto)
                # 5: rtf
                # 6: estado
                # 7: anotacion
                # 8: numero
                # 9: profesional (mariana)

                paciente = Paciente.objects.get(idaccess=datos[1])

                # Fecha y hora
                fecha_str = datos[2]
                hora_str = datos[3]
                fecha_obj = datetime.strptime(f"{fecha_str} {hora_str}", "%d/%m/%Y %H:%M")

                historia_texto = datos[4].replace("\n", "")
                diagnostico = datos[6].replace("\n", "")
                tratamiento = datos[7].replace("\n", "")

                historia = HistoriaClinica(
                    paciente=paciente,
                    idaccess=datos[1],
                    fecha=fecha_obj,
                    historia=historia_texto,
                    diagnostico=diagnostico,
                    tratamiento=tratamiento,
                    primeravez=False,
                    responsable=usuario
                )

                historias_a_insertar.append(historia)

            except Exception as e:
                print("Error procesando línea:")
                print(linea)
                print("Datos:", datos)
                print("Error:", str(e))
                continue

        fin = time.time()
        print("Ejecución en", fin - inicio, "segundos")

    if historias_a_insertar:
        HistoriaClinica.objects.bulk_create(historias_a_insertar)
        print(f"Se insertaron {len(historias_a_insertar)} historias clínicas.")


if __name__ == "__main__":
    cargar_hc("Historiasultimas.txt")
