autenticacion_simpĺe = {
    "admin" : "password",
    "jorge" : "aceval",
    "joaquin" : "viveros"
}



def register ():
    #Lógica de autenticación simple.
    user = input("Ingrese su nombre de usuario: ")

    if not user:
        print("Error: Nombre de usuario y contraseña no pueden estar vacíos.")
        return

    if user in autenticacion_simpĺe:
        print("Error: El nombre de usuario ya existe.")
        return

    password = input("Ingrese su contraseña: ").strip()

    if not password:
        print("Error: Nombre de usuario y contraseña no pueden estar vacíos.")
        return
    
    autenticacion_simpĺe[user] = password
    print("Registro exitoso. Ahora puede iniciar sesión.")

    

    


