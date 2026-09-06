
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
        user = input("Ingrese su nombre de usuario: ")
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



def login (user, password):
    #Lógica de inicio de sesión simple.
    if user in autenticacion_simple and autenticacion_simple[user] == password:
        print("Inicio de sesión exitoso.")
        return True
    else:
        print("Error: Nombre de usuario o contraseña incorrectos.")
        return False

    

    


