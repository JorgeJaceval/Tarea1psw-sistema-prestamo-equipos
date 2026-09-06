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
            #Lógica para administrar usuarios existentes
            continue

        if op == 3:
            print("Registrando un nuevo equipo...")
            #Lógica para registrar un nuevo equipo
            continue

        if op == 4:
            print("Consultando equipos existentes...")
            #Lógica para consultar equipos existentes
            continue

        if op == 5:
            print("Aprobando / rechazando préstamos...")
            #Lógica para aprobar / rechazar préstamos
            continue

        if op == 6:
            print("Consultando préstamos existentes...")
            #Lógica para consultar préstamos existentes
            continue

        if op == 7:
            print("Ingresando devoluciones...")
            #Lógica para ingresar devoluciones
            continue

        if op == 0:
            print("Saliendo del sistema...")
            exit()

        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")




def menu_autenticacion ():
    while True:
        print ("1. Registrar")
        print ("2. Iniciar sesión")
        print ("3. Salir")

        option = input("Ingrese el número de la opción que desea seleccionar: ")

        if option == "1":
            auth.register()
            continue

        elif option == "2":
            print("Iniciando sesion...")
            usuario = input("Ingrese su nombre de usuario: ").strip()
            password = input("Ingrese su contraseña: ").strip()

            if not auth.login(usuario, password):
                continue
            else:
                return usuario
        
        elif option == "3":
            print("Saliendo del sistema...")
            exit()
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")
            


def menu_usuario (user):
    #Funcionalidades: Consultar equipos, solicitar préstamos y consultar préstamos.
    #Comprobar antes si tiene prestamos atrasados

    print ("Comprobando si tiene préstamos atrasados...")
    #Ir a la base de datos y comprobar si tiene prestamos atrasados
    #Si tiene prestamos atrasados, no puede solicitar nuevos prestamos.
    prestamos.prestamos_activos(user)

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
            continue

        if op == 2:
            print("Solicitando un préstamo...")
            #Lógica para solicitar un préstamo
            continue

        if op == 3:
            print("Consultando mis préstamos existentes...")
            #Ir a la base de datos y consultar los préstamos del usuario
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
