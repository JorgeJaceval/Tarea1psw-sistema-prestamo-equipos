
'''
"admin" : {
    "password" : "hash",
    "rol" : "admin"
}
'''
autenticacion_simple = {

}

def register ():
    #Lógica de autenticación simple.
    while True:
        user = input("Ingrese su nombre de usuario: ").strip()
        print()

        if not user:
            print("Error: Nombre de usuario y contraseña no pueden estar vacíos.")
            continue

        if user in autenticacion_simple:
            print("Error: El nombre de usuario ya existe.")
            continue

        password = input("Ingrese su contraseña: ").strip()

        if not password:
            print("Error: Nombre de usuario y contraseña no pueden estar vacíos.")
            continue
        
        #Todos los usuarios registrados tendrán el rol de "user" por defecto.
        
        autenticacion_simple[user] = {"password": password, "rol": "user"}

        print("Registro exitoso. Ahora puede iniciar sesión.")
        return



def login (user, password):
    #Lógica de inicio de sesión simple.
    if user in autenticacion_simple and autenticacion_simple[user]["password"] == password:
        print("Inicio de sesión exitoso.")
        return True
    else:
        print("Error: Nombre de usuario o contraseña incorrectos.")
        return False

    

    

def administrar_usuarios():
    if not autenticacion_simple:
        print("No hay usuarios registrados.")
        return

    usuarios = list(autenticacion_simple.keys())

    for indice, user in enumerate(usuarios, start=1):
        rol = autenticacion_simple[user]["rol"]
        print(f"{indice}. {user} - Rol: {rol}")

    op = input("Ingrese el número del usuario que desea eliminar o actualizar (o '0' para salir): ")

    if not op.isdigit():
        print("Opción no válida.")
        return

    seleccion = int(op)

    if seleccion == 0:
        return

    if seleccion < 1 or seleccion > len(usuarios):
        print("Usuario no válido.")
        return

    user1 = usuarios[seleccion - 1]
    print(f"Usuario seleccionado: {user1}")

    print("1. Eliminar usuario")
    print("2. Actualizar rol")
    print("0. Cancelar")

    accion = input("Seleccione una acción: ")

    if accion == "1":
        del autenticacion_simple[user1]
        print("Usuario eliminado correctamente.")

    elif accion == "2":
        nuevo_rol = input("Ingrese el nuevo rol (admin/user): ").strip()

        if nuevo_rol not in ["admin", "user"]:
            print("Rol no válido.")
            return

        autenticacion_simple[user1]["rol"] = nuevo_rol
        print("Rol actualizado correctamente.")

    elif accion == "0":
        return

    else:
        print("Opción no válida.")
    
