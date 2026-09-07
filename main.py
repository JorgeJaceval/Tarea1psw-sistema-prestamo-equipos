#Interfaz Menú via CLI.
import auth
import prestamos

def menu_admin ():
    #Funcionalidades: Registrar y administrar usuarios


    op = -1
    while op != 0:
        print("Opciones disponibles para admin:\n")
        print("-----Administración de usuarios-----")
        print("1. Registrar un nuevo usuario")
        print("2. Administrar usuarios existentes\n")

        print ("-----Opciones de equipos----")

        print ("3. Registrar un nuevo equipo")
        print ("4. Consultar equipos existentes\n")

        print ("-----Opciones de préstamos----")
        print ("5. Aprobar / rechazar prestamos")
        print ("6. Consultar prestamos existentes")
        print ("7. Ingresar devoluciones\n")

        print ("0. Salir")

        op = -1
        op = int(input("Seleccione una opción: "))

        if op == 1:
            auth.register()
            continue

        if op == 2:
            print("Administrando usuarios existentes...")
            auth.administrar_usuarios()
            continue

        if op == 3:
            print("Registrando un nuevo equipo...")
            prestamos.ingresar_equipo(input("Ingrese el nombre del equipo: "), input("Ingrese la cantidad de existencias: "))
            continue

        if op == 4:
            print("Consultando equipos existentes...")
            equipos = prestamos.mostrar_equipos_disponibles()

            if not equipos:
                print("No hay equipos disponibles.")
                continue

            for equipo in equipos:
                print(f" - {equipo[1]} (Disponibles: {equipo[3]})")
            print("")
            continue

        if op == 5:
            print("Aprobando / rechazando préstamos...")
            prestamos.administrar_prestamos()
            continue

        if op == 6:
            print("Consultando préstamos existentes...")
            prestamos.prestamos_activos_total()
            continue

        if op == 7:
            print("Ingresando devoluciones...")
            prestamos.devolver_prestamo(input("Ingrese el ID del préstamo a devolver: "))

            continue

        if op == 0:
            print("Saliendo del sistema...")
            exit()

        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")




def menu_autenticacion ():
    while True:
        print ("Opciones disponibles:\n")
        print ("1. Iniciar sesión")
        print ("2. Salir \n")

        option = input("Ingrese el número de la opción que desea seleccionar: ")

        if option == "1":
            print("\nIniciando sesion...\n")
            usuario = input("Ingrese su nombre de usuario: ").strip()
            password = input("Ingrese su contraseña: ").strip()

            if not auth.login(usuario, password):
                continue
            else:
                return usuario
        
        elif option == "2":
            print("\nSaliendo del sistema...")
            exit()
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")
            


def menu_usuario (user_id):
    #Funcionalidades: Consultar equipos, solicitar préstamos y consultar préstamos.

    

    

    op = -1
    while op != 0:
        op = -1
        print("Opciones disponibles Usuario")
        print("1. Consultar equipos disponibles")
        print("2. Solicitar un préstamo")
        print("3. Consultar mis préstamos existentes / solicitudes")
        print("0. Salir \n")

        op = int(input("Seleccione una opción: "))
        print ("")

        if op == 1:
            print("Consultando equipos disponibles...")
            #Ir a la base de datos y consultar los equipos disponibles
            equipos = prestamos.mostrar_equipos_disponibles()

            if not equipos:
                print("No hay equipos disponibles.")
                continue

            for equipo in equipos:
                print(f" - {equipo[1]} (Disponibles: {equipo[3]})")
            print ("")
            
            continue

        if op == 2:
            #Comprobar antes si tiene prestamos atrasados
            if auth.autenticacion_simple[auth.obtener_usuario_por_id(user_id)]["multa"] > 0:
                print("No puede solicitar nuevos préstamos debido a que tiene una multa impuesta. \n")
                continue

            print ("Comprobando si puede solicitar nuevos préstamos...\n")
            #Ir a la base de datos y comprobar si tiene prestamos atrasados
            #Si tiene prestamos atrasados, no puede solicitar nuevos prestamos.
            prestamos_activos = prestamos.prestamos_activos(user_id)
            prestamos_pendientes = prestamos.prestamos_pendientes(user_id)

            if len(prestamos_activos) == 0:
                print("No tiene préstamos activos. \n")
                
            elif len(prestamos_activos) >= 3:
                print("El máximo son 3 prestamos. No puede solicitar nuevos préstamos hasta que devuelva uno. \n")
                continue

            elif len(prestamos_activos) < 3:
                print(f"No ha superado el máximo de prestamos ({len(prestamos_activos)}|3), puede solicitar hasta {3 - len(prestamos_activos)} préstamo(s). \n")

            if len(prestamos_pendientes) >= 3:
                print("Tiene 3 solicitudes pendientes. No puede enviar más solicitudes hasta que un administrador revise alguna. \n")
                continue

            print("Solicitando un préstamo...\n")

            equipos = prestamos.mostrar_equipos_disponibles()
            if not equipos:
                print("No hay equipos disponibles para solicitar.")
                continue

            for indice, equipo in enumerate(equipos, start=1):
                print(f"{indice}. {equipo[1]} (Disponibles: {equipo[3]})")
            print ("")

            seleccion = input("Ingrese el número del equipo que desea solicitar:")

            if not seleccion.isdigit():
                print("Opción no válida.")
                continue

            seleccion = int(seleccion)

            if seleccion < 1 or seleccion > len(equipos):
                print("Equipo no válido.")
                continue

            equipo = equipos[seleccion - 1]
            prestamos.solicitar_prestamo(user_id, equipo)
            continue

        if op == 3:
            print("Consultando mis préstamos existentes / solicitudes...")
            prestamos_usuario = prestamos.prestamos_usuario(user_id)

            if len(prestamos_usuario) == 0:
                print("No tiene préstamos ni solicitudes registradas.")
            else:
                print("Tiene préstamos / solicitudes registradas:")
                print("")
                for prestamo in prestamos_usuario:
                    print(f"ID: {prestamo[0]} | Equipo: {prestamo[1]} | Estado: {prestamo[5]}")
                print ("")

            continue

        if op == 0:
            print("Saliendo del sistema...")
            exit()

        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")



def main ():
    #Funcionalidad principal del sistema.
    print("****************************************************")
    print("*  Bienvenido al sistema de préstamos de equipos.  *")
    print("****************************************************\n")
    
    usuario = menu_autenticacion()
    usuario_autenticado = auth.autenticacion_simple[usuario]
    rol = usuario_autenticado["rol"]
    user_id = usuario_autenticado["id"]

    if rol == "admin":
        menu_admin()
    else:
        menu_usuario(user_id)


if __name__ == "__main__":
    main()
