
import datetime
import difflib
import time
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "esteticabarbetti.settings")
django.setup()

from pacientes.models import Paciente


def limpiar(valor):
    if valor is None:
        return None
    valor = valor.strip()
    return valor if valor != "" else None


def cargar_pacientes(archivo_txt):
    inicio = time.time()
    pacientes = []
    a = 0
    c = 0
    with open(archivo_txt, "r", encoding="latin-1") as f:
        for linea in f:
            datos = linea.strip().split(";")

            existe = Paciente.objects.filter(
                nombre=datos[1],
                domicilio=datos[6],
                telefono=datos[9]
            ).exists()

            if existe:
                a = a + 1
            else:

                existe = Paciente.objects.get(
                    nombre=datos[1],
                    domicilio=datos[6],
                    telefono=datos[9]
                )

                if datos[1] == existe.nombre:
                    print("SIPP")
                
                
                
                
                
                """
                paciente=Paciente(
                    idaccess=datos[0],
                    nombre=datos[1],
                    fechanacimiento=datetime.datetime.strptime(limpiar(datos[2]), "%d/%m/%Y").date() if limpiar(datos[2]) else None,
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
                
                pacientes.append(paciente)
                """
                c = c + 1

    """
    try:
        Paciente.objects.bulk_create(pacientes)
    except Exception as e: 
        print("Ocurrió un error:", e)
    """ 
    fin = time.time()
    diferencia = fin - inicio
    print("Tiempo de ejecucion " + str(diferencia))        
    print("Pacientes: " + str(c))
    print("Excluidos: " + str(a))

if __name__ == "__main__":
    cargar_pacientes("Identificacion.txt")
