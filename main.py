#Interfaz Menú via CLI.
import auth
import prestamos

def menu_admin ():
    #Funcionalidades: Registrar y administrar usuarios
    print("Opciones disponibles para admin:")
    print("-----Administración de usuarios-----")
    print("1. Registrar un nuevo usuario")
    print("2. Administrar usuarios existentes")

    print ("\n -----Opciones de equipos----")

    print ("3. Registrar un nuevo equipo")
    print ("4. Consultar equipos existentes")

    print ("\n -----Opciones de préstamos----")
    print ("5. Aprobar / rechazar prestamos")
    print ("6. Consultar prestamos existentes")
    print ("7. Ingresar devoluciones")

    print ("\n 0. Salir")

    op = -1
    while op != 0:
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
            prestamos.mostrar_equipos_disponibles()
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
        print ("1. Iniciar sesión")
        print ("2. Salir")

        option = input("Ingrese el número de la opción que desea seleccionar: ")

        if option == "1":
            print("Iniciando sesion...")
            usuario = input("Ingrese su nombre de usuario: ").strip()
            password = input("Ingrese su contraseña: ").strip()

            if not auth.login(usuario, password):
                continue
            else:
                return usuario
        
        elif option == "2":
            print("Saliendo del sistema...")
            exit()
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")
            


def menu_usuario (user):
    #Funcionalidades: Consultar equipos, solicitar préstamos y consultar préstamos.
    #Comprobar antes si tiene prestamos atrasados

    print ("Comprobando si puede solicitar nuevos préstamos...")
    #Ir a la base de datos y comprobar si tiene prestamos atrasados
    #Si tiene prestamos atrasados, no puede solicitar nuevos prestamos.
    prestamos_activos = prestamos.prestamos_activos(user)

    if len(prestamos_activos) >= 3:
        print("El máximo son 3 prestamos activos. No puede solicitar nuevos préstamos hasta que devuelva una.")
        return

    if len(prestamos_activos) < 3:
        print("No tiene préstamos activos / no ha superado el máximo, puede solicitar nuevos préstamos.")
    

    

    op = -1
    while op != 0:
        op = -1
        print("Opciones disponibles")
        print("1. Consultar equipos disponibles")
        print("2. Solicitar un préstamo")
        print("3. Consultar mis préstamos existentes")
        print("0. Salir")

        op = int(input("Seleccione una opción: "))

        if op == 1:
            print("Consultando equipos disponibles...")
            #Ir a la base de datos y consultar los equipos disponibles
            equipos = prestamos.mostrar_equipos_disponibles()
            for equipo in equipos:
                print(f" - {equipo[1]} (Disponibles: {equipo[3]})")
            
            continue

        if op == 2:
            print("Solicitando un préstamo...")
            equipo = input("Ingrese el nombre del equipo que desea solicitar: ")
            prestamos.solicitar_prestamo(user, equipo)
            continue

        if op == 3:
            print("Consultando mis préstamos existentes...")
            print ("Sus prestamos activos son: \n")
            print (prestamos_activos)

            continue

        if op == 0:
            print("Saliendo del sistema...")
            exit()

        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")



def main ():
    #Funcionalidad principal del sistema.
    print("Bienvenido al sistema de préstamos de equipos.")
    
    usuario = menu_autenticacion()
    rol = auth.autenticacion_simple[usuario]["rol"]

    if rol == "admin":
        menu_admin()
    else:
        menu_usuario(usuario)


if __name__ == "__main__":
    main()
