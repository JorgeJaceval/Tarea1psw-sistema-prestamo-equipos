Jorge Aceval 202273513-9
Joaquin Viveros 202273586-4

## Cómo ejecutar el programa

Necesitas Python 3.7 o superior. Abre una terminal en la carpeta donde está `main.py`, instala las dependencias y ejecuta:

```bash
python -m pip install -r requirements.txt
python main.py
```

Si tu instalación usa `python3` o `py`, reemplaza `python` en los comandos. Ejecuta siempre desde la carpeta del proyecto, porque ahí se buscan `bd_equipos.csv` y `bd_prestamos.csv`.

## Usuarios

El programa no publica usuarios ni contraseñas en el código. Al primer inicio, si no existe `bd_usuarios.csv`, el sistema solicita crear un administrador inicial por consola.



## Para probarlo

Al iniciar, escribe `1` para entrar con el administrador local que creaste.

El administrador gestiona usuarios, equipos y préstamos. La opción `6` muestra los préstamos activos.

El usuario puede consultar equipos, pedir préstamos y revisar sus solicitudes. Las multas y los préstamos vencidos bloquean las nuevas solicitudes.

Para salir, escribe `0` en el menú de tu cuenta o `2` en la pantalla inicial. Para cambiar de cuenta, vuelve a ejecutar el programa.

Los cambios de equipos y préstamos quedan guardados en los CSV. Los usuarios, roles y multas quedan guardados localmente en `bd_usuarios.csv`.

## Dónde está cada cosa

- `main.py`: menús y ejecución del programa.
- `auth.py`: usuarios, inicio de sesión, roles y multas.
- `prestamos.py`: equipos, solicitudes, devoluciones y lectura de los CSV.
- `monitoreo.py`: configuración de logs y Sentry.

## Logs

Los registros quedan en `logs/sistema.log`, con fecha, nivel y módulo. `INFO` indica una operación normal, `WARNING` una advertencia y `ERROR` un fallo con su detalle. El archivo rota al llegar a aproximadamente 1 MB y guarda hasta tres copias. Los logs no se suben a Git y los registros de operaciones no incluyen contraseñas.

Para verlos mientras pruebas, abre otra terminal de PowerShell en la carpeta del proyecto:

```powershell
Get-Content .\logs\sistema.log -Wait -Tail 20
```

## Conectar Sentry

La configuración está en [`monitoreo.py`](monitoreo.py), dentro de `configurar_monitoreo()`. Ahí se leen `SENTRY_DSN` y `SENTRY_ENVIRONMENT`, y se llama a `sentry_sdk.init()`. Si necesitas cambiar las opciones de la integración, ese es el lugar.

Para conectarlo a tu cuenta, crea un proyecto de Python en [Sentry](https://sentry.io/) y copia su DSN, la dirección que identifica el proyecto. **Reemplaza `TU_DSN` en el siguiente comando de PowerShell** y ejecuta todo en la misma terminal:

```powershell
$env:SENTRY_DSN = "TU_DSN"
$env:SENTRY_ENVIRONMENT = "desarrollo"
python main.py
```

El DSN se configura en la terminal; no es necesario escribirlo en el archivo Python. Estas variables duran hasta cerrar la terminal. `SENTRY_ENVIRONMENT` es opcional y usa `desarrollo` por defecto. En Linux o macOS puedes definirlas con `export SENTRY_DSN="TU_DSN"` y `export SENTRY_ENVIRONMENT="desarrollo"`.

Sentry recibe los errores y el contexto de los logs, sin capturar variables locales ni fragmentos del código. Sin DSN, solo se generan logs locales. Revisa `logs/sistema.log`: debe aparecer `Sentry activado` cuando la configuración se haya cargado. Eso confirma el inicio del SDK; la recepción de errores se comprueba en tu proyecto de Sentry.

## Pruebas

```bash
python -m unittest discover -s tests -v
```

Las pruebas usan eventos en memoria y no envían datos a Sentry. Si falta el SDK, se omiten las dos pruebas que lo necesitan.
