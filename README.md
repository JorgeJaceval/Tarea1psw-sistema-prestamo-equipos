Jorge Aceval 202273513-9
Joaquin Viveros 202273586-4

## Cómo ejecutar el programa

Necesitas tener Python 3.7 o superior instalado. El programa funciona desde la terminal. Para instalar el SDK de Sentry, ejecuta una vez desde la carpeta del proyecto:

```bash
python -m pip install -r requirements.txt
```

Las dependencias están en `requirements.txt`.

Abre una terminal dentro de la carpeta del proyecto, donde está `main.py`, y ejecuta:

```bash
python main.py
```

Si en tu equipo Python se ejecuta con `python3`, usa:

```bash
python3 main.py
```

En Windows también puedes usar `py main.py` si tienes instalado el lanzador de Python. Si ninguno de estos comandos se reconoce, revisa que Python esté instalado y agregado al PATH.

Ejecuta el programa desde esa carpeta: ahí busca los archivos `bd_equipos.csv` y `bd_prestamos.csv`, que ya vienen en el repositorio.

## Para probarlo

Al iniciar, escribe `1` para entrar. Puedes usar estas cuentas:

| Rol | Usuario | Contraseña |
| --- | --- | --- |
| Administrador | `admin` | `admin123` |
| Usuario | `juan` | `juan123` |

Con la cuenta de administrador puedes gestionar usuarios y equipos, aprobar o rechazar solicitudes y registrar devoluciones. Para consultar los préstamos activos, elige la opción `6`.

Con la cuenta de usuario puedes consultar equipos, pedir un préstamo y revisar tus solicitudes. Si tienes una multa o un préstamo activo vencido, el sistema bloquea las nuevas solicitudes.

Para salir, escribe `0` en el menú de tu cuenta. Si quieres entrar con otra cuenta, vuelve a ejecutar el programa. En la pantalla inicial, la opción para salir es `2`.

Los cambios de equipos y préstamos quedan guardados en los CSV. Los usuarios nuevos, los cambios de rol y las multas se mantienen solo mientras el programa está abierto; al reiniciarlo se cargan otra vez los valores de `auth.py`.

## Logs

Al ejecutar el programa se crea `logs/sistema.log`. Ahí quedan los inicios de sesión, las consultas, los cambios de usuarios y equipos, las solicitudes, las devoluciones y los errores. Cada línea incluye la fecha, el nivel y el módulo que la generó.

`INFO` indica una operación normal, `WARNING` una situación como un acceso fallido o una solicitud bloqueada, y `ERROR` un fallo inesperado. Estos últimos incluyen el detalle del error para poder revisarlo.

El archivo rota al llegar a aproximadamente 1 MB y conserva hasta tres copias anteriores. La carpeta `logs` está excluida de Git. Los registros de operaciones usan los IDs de los usuarios y no incluyen sus contraseñas.

Para ver el archivo mientras pruebas el programa, puedes abrir otra terminal de PowerShell en la carpeta del proyecto y ejecutar:

```powershell
Get-Content .\logs\sistema.log -Wait -Tail 20
```

## Conectar Sentry

Sentry permite revisar los errores del programa desde su sitio web. Los logs locales funcionan aunque todavía no tengas una cuenta o no hayas configurado Sentry.

Para conectarlo, crea una cuenta en [Sentry](https://sentry.io/), crea un proyecto de Python y copia su DSN. Es la dirección que Sentry entrega para que el programa envíe los errores a ese proyecto. Puedes consultar la [guía del SDK oficial](https://pypi.org/project/sentry-sdk/) para la instalación y configuración inicial.

En PowerShell, reemplaza `TU_DSN` por esa dirección y ejecuta el programa desde la misma terminal:

```powershell
$env:SENTRY_DSN = "TU_DSN"
$env:SENTRY_ENVIRONMENT = "desarrollo"
python main.py
```

En Linux o macOS:

```bash
export SENTRY_DSN="TU_DSN"
export SENTRY_ENVIRONMENT="desarrollo"
python3 main.py
```

Estas variables duran lo que dure la sesión de la terminal. No hace falta poner el DSN en el código. `SENTRY_ENVIRONMENT` es opcional y su valor por defecto es `desarrollo`.

Con Sentry activo, los registros de nivel `ERROR` se envían como errores y los `INFO` y `WARNING` quedan como contexto de lo que ocurrió antes. Los fallos inesperados se registran antes de cerrar el programa. Se desactivó la captura de variables locales y fragmentos del código para evitar que se incluyan las credenciales que usa este proyecto.

Para comprobar el envío, con el SDK instalado y el DSN configurado, ejecuta:

```bash
python -c "from monitoreo import configurar_monitoreo; import logging; sentry = configurar_monitoreo(); logging.error('Prueba de conexion con Sentry'); sentry.flush(timeout=5) if sentry else print('Sentry no esta activo; revisa logs/sistema.log')"
```

El evento `Prueba de conexion con Sentry` debería aparecer en los errores de tu proyecto. Si no aparece, revisa el DSN y la conexión a internet. En `logs/sistema.log` puedes comprobar si Sentry se activó, quedó sin configurar o faltó instalar el SDK.

Para ejecutar las pruebas automáticas:

```bash
python -m unittest discover -s tests -v
```

Las pruebas de Sentry usan un transporte en memoria: no necesitan una cuenta ni envían eventos a internet. Si no instalaste el SDK, esas dos pruebas se omiten.
