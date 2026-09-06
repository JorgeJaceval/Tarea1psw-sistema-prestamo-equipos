# BD equipos.csv
#id  | equipos | existencias totales | existencias disponibles
# BD prestamos.csv
#id | equipo | id_usuario |fecha_desde |fecha_hasta | estado 
import csv
from datetime import date, datetime, timedelta
import auth
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


def prestamos_activos (user_id):
    prestamos = []
    for row in leer_prestamos():
        if len(row) >= 6 and row[2] == str(user_id) and row[5] == 'activo':
            prestamos.append(row)
    return prestamos


def prestamos_pendientes (user_id):
    prestamos = []
    for row in leer_prestamos():
        if len(row) >= 6 and row[2] == str(user_id) and row[5] == 'pendiente':
            prestamos.append(row)
    return prestamos


def prestamos_usuario (user_id):
    prestamos = []
    for row in leer_prestamos():
        if len(row) >= 6 and row[2] == str(user_id):
            prestamos.append(row)
    return prestamos


def prestamos_activos_total ():
    prestamos = []
    for row in leer_prestamos():
        if len(row) >= 6 and row[5] == 'activo':
            prestamos.append(row)
    return prestamos

def leer_prestamos():
    prestamos = []
    with open('bd_prestamos.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            prestamos.append(row)
    return prestamos


def guardar_prestamos(prestamos):
    with open('bd_prestamos.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(prestamos)

#Solicitud de prestamo de un equipo por parte de un usuario.
def solicitar_prestamo (user_id, equipo):
    solicitudes_pendientes = prestamos_pendientes(user_id)

    if len(solicitudes_pendientes) >= 3:
        print("El máximo son 3 solicitudes pendientes. Espere a que un administrador revise sus solicitudes antes de enviar otra.")
        return

    if len(equipo) < 4:
        print("Equipo no válido.")
        return

    if int(equipo[3]) <= 0:
        print("No hay existencias disponibles. No se puede solicitar el préstamo.")
        return

    print("Hay existencias disponibles. Se puede solicitar el préstamo.")

    fecha_desde = date.today()
    fecha_hasta = fecha_desde + timedelta(days=14)

    with open('bd_prestamos.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([obtener_siguiente_id('bd_prestamos.csv'), equipo[1], user_id, fecha_desde, fecha_hasta, "pendiente"])
        print("Solicitud de préstamo enviada. Espere la aprobación del administrador.\n")



def mostrar_equipos_disponibles():

    equipos_disponibles = []
    with open('bd_equipos.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 4 and int(row[3]) > 0:
                equipos_disponibles.append(row)
    return equipos_disponibles

def actualizar_existencias(equipo, cambio):
    equipos = []
    with open('bd_equipos.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 4 and row[1] == equipo:
                row[3] = str(int(row[3]) + cambio)  # Actualizar existencias disponibles
            equipos.append(row)

    with open('bd_equipos.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(equipos)


def obtener_existencias_disponibles(equipo):
    with open('bd_equipos.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 4 and row[1] == equipo:
                return int(row[3])
    return 0


#---Funcionalidades de administrador.---
#Ingresa un nuevo equipo a la base de datos de equipos.
def ingresar_equipo(equipo, existencias):
    with open('bd_equipos.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([obtener_siguiente_id('bd_equipos.csv'), equipo, existencias, existencias])
        print("Equipo ingresado exitosamente.")


def administrar_prestamos():
    prestamos = leer_prestamos()
    prestamos_pendientes = []

    for row in prestamos:
        if len(row) >= 6 and row[5] == 'pendiente':
            prestamos_pendientes.append(row)

    if not prestamos_pendientes:
        print("No hay préstamos pendientes.")
        return

    for indice, prestamo in enumerate(prestamos_pendientes, start=1):
        print(f"{indice}. ID: {prestamo[0]}, Equipo: {prestamo[1]}, ID usuario: {prestamo[2]}, Estado: {prestamo[5]}")

    op = input("Ingrese el número del préstamo que desea aprobar o rechazar (o '0' para salir): ")

    if not op.isdigit():
        print("Opción no válida.")
        return

    seleccion = int(op)

    if seleccion == 0:
        return

    if seleccion < 1 or seleccion > len(prestamos_pendientes):
        print("Selección no válida.")
        return

    prestamo_seleccionado = prestamos_pendientes[seleccion - 1]
    decision = input("Ingrese 'A' para aprobar o 'R' para rechazar el préstamo: ").strip().upper()

    if decision == 'A':
        existencias_disponibles = obtener_existencias_disponibles(prestamo_seleccionado[1])

        if existencias_disponibles <= 0:
            print("No hay existencias disponibles para aprobar este préstamo.")
            print("Debe rechazar la solicitud o esperar a que se devuelva una unidad del equipo.")
            return

        # Aprobar el préstamo
        prestamo_seleccionado[5] = 'activo'
        # Actualizar existencias en bd_equipos.csv
        actualizar_existencias(prestamo_seleccionado[1], -1)
        print("Préstamo aprobado.")
    
    elif decision == 'R':
        # Rechazar el préstamo
        prestamo_seleccionado[5] = 'cancelado'
        print("Préstamo cancelado.")
    else:
        print("Decisión no válida.")
        return

    # Guardar los cambios en bd_prestamos.csv
    guardar_prestamos(prestamos)
                       
def devolver_prestamo(prestamo_id):
    prestamos = leer_prestamos()
    prestamo_encontrado = False

    for row in prestamos:
        if len(row) >= 6 and row[0] == prestamo_id:
            if row[5] == 'activo':
                try:
                    fecha_hasta = datetime.strptime(row[4], "%Y-%m-%d").date()
                except ValueError:
                    print("La fecha de devolución del préstamo no tiene un formato válido.")
                    return

                dias_atraso = (date.today() - fecha_hasta).days
                multa = 1 if dias_atraso > 14 else 0

                if not auth.aplicar_multa(row[2], multa):
                    print("No se encontró el usuario asociado al préstamo.")
                    return

                row[5] = 'finalizado'
                actualizar_existencias(row[1], 1)  # Incrementar existencias disponibles
                prestamo_encontrado = True
                print("Préstamo devuelto exitosamente.")
                if multa == 1:
                    print("El usuario tiene una multa por atraso mayor a dos semanas.")
                break
            else:
                print("El préstamo no está activo y no puede ser devuelto.")
                return

    if not prestamo_encontrado:
        print("No se encontró un préstamo con el ID proporcionado.")
        return

    # Guardar los cambios en bd_prestamos.csv
    guardar_prestamos(prestamos)
