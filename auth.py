from getpass import getpass
import logging

logger = logging.getLogger(__name__)
'''
"admin" : {
    "id" : 1,
    "password" : "hash",
    "rol" : "admin",
    "multa" : 0
}
'''
autenticacion_simple = {
    "admin": {
        "id" : 1,
        "password": "admin123",
        "rol": "admin",
        "multa": 0
    },
    "joaco": {
        "id" : 2,
        "password": "joaco123",
        "rol": "user",
        "multa": 1
    },
    "juan": {
        "id" : 3,
        "password": "juan123",
        "rol": "user",
        "multa": 0
    },
    "maria": {
        "id" : 4,
        "password": "maria123",
        "rol": "user",
        "multa": 0
    },
    "pedro": {
        "id" : 5,
        "password": "pedro123",
        "rol": "user",
        "multa": 0
    },
    "ana": {
        "id" : 6,
        "password": "ana123",
        "rol": "user",
        "multa": 0
    }

}

def obtener_siguiente_id_usuario():
    mayor_id = 0

    for datos in autenticacion_simple.values():
        if "id" in datos:
            mayor_id = max(mayor_id, int(datos["id"]))

    return mayor_id + 1


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

        password = getpass("Ingrese su contraseña: ")

        if not password:
            print("Error: Nombre de usuario y contraseña no pueden estar vacíos.")
            continue
        
        #Todos los usuarios registrados tendrán el rol de "user" por defecto.
        
        autenticacion_simple[user] = {
            "id": obtener_siguiente_id_usuario(),
            "password": password,
            "rol": "user",
            "multa": 0
        }

        logger.info("Usuario registrado: usuario_id=%s", autenticacion_simple[user]["id"])
        print("Registro exitoso. Ahora puede iniciar sesión.")
        return



def login (user, password):
    #Lógica de inicio de sesión simple.
    if user in autenticacion_simple and autenticacion_simple[user]["password"] == password:
        logger.info("Inicio de sesion: usuario_id=%s rol=%s", autenticacion_simple[user]["id"], autenticacion_simple[user]["rol"])
        print("Inicio de sesión exitoso.\n ")
        return True
    else:
        logger.warning("Intento de inicio de sesion fallido")
        print("Error: Nombre de usuario o contraseña incorrectos, intente nuevamente. \n")
        return False

    

    
def obtener_usuario_por_id(user_id):
    for user, datos in autenticacion_simple.items():
        if datos["id"] == int(user_id):
            return user
    return None


def aplicar_multa(user_id, multa):
    user = obtener_usuario_por_id(user_id)

    if user is None:
        logger.warning("No se pudo actualizar la multa: usuario inexistente")
        return False

    autenticacion_simple[user]["multa"] = multa
    logger.info("Multa actualizada: usuario_id=%s multa=%s", autenticacion_simple[user]["id"], multa)
    return True


def administrar_usuarios():
    if not autenticacion_simple:
        print("No hay usuarios registrados.")
        return

    usuarios = list(autenticacion_simple.keys())

    for indice, user in enumerate(usuarios, start=1):
        user_id = autenticacion_simple[user]["id"]
        rol = autenticacion_simple[user]["rol"]
        multa = autenticacion_simple[user]["multa"]
        print(f"{indice}. {user} - ID: {user_id} - Rol: {rol} - Multa: {multa}")

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
        user_id = autenticacion_simple[user1]["id"]
        del autenticacion_simple[user1]
        logger.info("Usuario eliminado: usuario_id=%s", user_id)
        print("Usuario eliminado correctamente.")

    elif accion == "2":
        nuevo_rol = input("Ingrese el nuevo rol (admin/user): ").strip()

        if nuevo_rol not in ["admin", "user"]:
            print("Rol no válido.")
            return

        autenticacion_simple[user1]["rol"] = nuevo_rol
        logger.info("Rol actualizado: usuario_id=%s rol=%s", autenticacion_simple[user1]["id"], nuevo_rol)
        print("Rol actualizado correctamente.")

    elif accion == "0":
        return

    else:
        print("Opción no válida.")
    
