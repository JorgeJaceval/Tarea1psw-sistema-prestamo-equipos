# BD equipos.csv
#id  | equipos | existencias totales | existencias disponibles
# BD prestamos.csv
#id | equipo_id | usuario |fecha_desde |fecha_hasta | estado 
import csv

#Determina la cantidad de prestamos activos de un solo usuario.

#--Funcionalidades de usuario.---
def obtener_siguiente_id(nombre_archivo):
    mayor_id = 0
    with open(nombre_archivo, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 1 and row[0].isdigit():
                mayor_id = max(mayor_id, int(row[0]))
    return mayor_id + 1


def prestamos_activos (user):
    prestamos = []
    with open('bd_prestamos.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 6 and row[2] == user and row[5] == 'activo':
                prestamos.append(row)
    return prestamos

#Solicitud de prestamo de un equipo por parte de un usuario.
def solicitar_prestamo (user, equipo):
    #Abrir primero el archivo de equipos, para saber si hay existencias

    with open ('bd_equipos.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 4 and row[1] == equipo:
                if int(row[3]) > 0:
                    #Hay existencias, se puede solicitar el préstamo
                    print("Hay existencias disponibles. Se puede solicitar el préstamo.")
                    #Se realiza el prestamo
                    with open('bd_prestamos.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([obtener_siguiente_id('bd_prestamos.csv'), equipo, user, "fecha_solicitud", "fecha_devolucion", "activo"])
                        print("Solicitud de préstamo enviada. Espere la aprobación del administrador.")
                    
                else:
                    print("No hay existencias disponibles. No se puede solicitar el préstamo.")
                    return
                    

def mostrar_equipos_disponibles():
    equipos_disponibles = []
    with open('bd_equipos.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 4 and int(row[3]) > 0:
                equipos_disponibles.append(row)
    return equipos_disponibles




#---Funcionalidades de administrador.---
#Ingresa un nuevo equipo a la base de datos de equipos.
def ingresar_equipo(equipo, existencias):
    with open('bd_equipos.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([obtener_siguiente_id('bd_equipos.csv'), equipo, existencias, existencias])
        print("Equipo ingresado exitosamente.")

def 