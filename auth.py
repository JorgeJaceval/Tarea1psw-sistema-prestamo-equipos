from getpass import getpass
import csv
import hashlib
import hmac
import logging
from pathlib import Path
import secrets

logger = logging.getLogger(__name__)
ARCHIVO_USUARIOS = Path("bd_usuarios.csv")
ITERACIONES_HASH = 100_000

autenticacion_simple = {}


def crear_hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        ITERACIONES_HASH
    ).hex()

    return salt, password_hash


def verificar_password(password, salt, password_hash):
    _, hash_ingresado = crear_hash_password(password, salt)
    return hmac.compare_digest(hash_ingresado, password_hash)


def cargar_usuarios():
    autenticacion_simple.clear()

    if not ARCHIVO_USUARIOS.exists():
        return

    with open(ARCHIVO_USUARIOS, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 6:
                user = row[0]
                autenticacion_simple[user] = {
                    "id": int(row[1]),
                    "salt": row[2],
                    "password_hash": row[3],
                    "rol": row[4],
                    "multa": int(row[5])
                }


def guardar_usuarios():
    with open(ARCHIVO_USUARIOS, "w", newline="") as file:
        writer = csv.writer(file)
        for user, datos in autenticacion_simple.items():
            writer.writerow([
                user,
                datos["id"],
                datos["salt"],
                datos["password_hash"],
                datos["rol"],
                datos["multa"]
            ])


def crear_admin_inicial():
    print("No hay usuarios registrados. Cree el administrador inicial.")

    while True:
        user = input("Ingrese nombre de administrador: ").strip()
        password = getpass("Ingrese contraseña del administrador: ")

        if not user or not password:
            print("Error: Usuario y contraseña no pueden estar vacíos.")
            continue

        salt, password_hash = crear_hash_password(password)
        autenticacion_simple[user] = {
            "id": 1,
            "salt": salt,
            "password_hash": password_hash,
            "rol": "admin",
            "multa": 0
        }
        guardar_usuarios()
        logger.info("Administrador inicial creado: usuario_id=1")
        print("Administrador inicial creado correctamente.\n")
        return


def inicializar_autenticacion():
    cargar_usuarios()

    if not autenticacion_simple:
        crear_admin_inicial()

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
        
        salt, password_hash = crear_hash_password(password)

        autenticacion_simple[user] = {
            "id": obtener_siguiente_id_usuario(),
            "salt": salt,
            "password_hash": password_hash,
            "rol": "user",
            "multa": 0
        }
        guardar_usuarios()

        logger.info("Usuario registrado: usuario_id=%s", autenticacion_simple[user]["id"])
        print("Registro exitoso. Ahora puede iniciar sesión.")
        return



def login (user, password):
    #Lógica de inicio de sesión simple.
    if user in autenticacion_simple and verificar_password(password, autenticacion_simple[user]["salt"], autenticacion_simple[user]["password_hash"]):
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
    guardar_usuarios()
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
        guardar_usuarios()
        logger.info("Usuario eliminado: usuario_id=%s", user_id)
        print("Usuario eliminado correctamente.")

    elif accion == "2":
        nuevo_rol = input("Ingrese el nuevo rol (admin/user): ").strip()

        if nuevo_rol not in ["admin", "user"]:
            print("Rol no válido.")
            return

        autenticacion_simple[user1]["rol"] = nuevo_rol
        guardar_usuarios()
        logger.info("Rol actualizado: usuario_id=%s rol=%s", autenticacion_simple[user1]["id"], nuevo_rol)
        print("Rol actualizado correctamente.")

    elif accion == "0":
        return

    else:
        print("Opción no válida.")
    
