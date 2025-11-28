
import datetime
import os
import django

# Configurar entorno Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "esteticabarbetti.settings")
django.setup()

from pacientes.models import Paciente


def limpiar(valor):
    if valor is None:
        return None
    valor = valor.strip()
    return valor if valor != "" else None


def cargar_pacientes(archivo_txt):
    with open(archivo_txt, "r", encoding="latin-1") as f:
        next(f)
        for linea in f:
            datos = linea.strip().split(";")

            fecha = datos[2].split(" ")
            
            print(len(datos))
            print(datos)
            Paciente.objects.create(
                    idaccess=datos[0],
                    nombre=datos[1],
                    fechanacimiento=datetime.datetime.strptime(limpiar(fecha[0]), "%d/%m/%Y").date() if limpiar(fecha[0]) else None,
                    sexo=datos[3],
                    estadocivil=datos[4],
                    numerodocumento=datos[5],
                    domicilio=datos[6],
                    correoelectronico=datos[7],
                    obrasocial=datos[8],
                    telefono=datos[9],
                    notas=datos[10],
                    proximoturno=datos[11],
                aviso=datos[12],
            )

            print(f"Paciente {datos[0]} insertado correctamente.")
        
if __name__ == "__main__":
    cargar_pacientes("pacientes.txt")
