Jorge Aceval 202273513-9
Joaquin Viveros 2022735


# Sistema de gestión de equipos 

## Análisis de requerimientos
Identificar al menos 8 ambigüedades, vacíos, riesgos o conflictos.
Algunas de las ambiguedadd presentes en este sistema podrían ser:

* Sistema de multas: No se especifica qué pasa en caso de qué alguien no entregue lo pedido en el tiempo establecido.
* Información del usuario que se debe almacernar en el sistrma
* Información de los equipos que se debe almacenar en el sistema
* Un riesgo posible es que una persona debe tener un límite en la cantidad de equipos posibles a pedir, ya que no puede reservar todo en un eventual caso
* Un riesgo posible es que la transición entre estados no sea correcta, lo cual provoque que hayan estados incorrectos que impidan reserver un equipo.
* Simple y confiable son criterios demasiados subjetivos, y no existe una forma de determinar cuándo el sistema cumple con ellos.
* Se menciona un sistema de autenticación, pero no cómo debe estar implementado, ni politicas de contraseñás
* Aprobación de solicitudes: no se establecen criterios para aprobar o rechazar una solicitud.

Formular preguntas que realizaría al cliente en base a las ambiguedades, riesgos,  vacios o conflicos
1. ¿Qué debe ocurrir cuando un usuario devuelve un equipo después de la fecha establecida? ¿Se aplicarán multas, restricciones o algún otro tipo de sanción?

2. ¿Qué información de cada usuario debe almacenarse obligatoriamente en el sistema?

3. ¿Qué información debe registrarse para cada equipo y qué dato permitirá identificarlo de manera única?

4. ¿Cuál es la cantidad máxima de equipos que una persona puede reservar o mantener prestados simultáneamente?

5. ¿Cuáles son los estados posibles de una solicitud o préstamo y qué transiciones están permitidas entre ellos?

6. ¿Qué criterios concretos permitirán considerar que el sistema es “simple” y “confiable”?

7. ¿Cómo deben administrarse las credenciales de los usuarios? ¿Existen requisitos mínimos o políticas para las contraseñas?

8. ¿Qué condiciones debe cumplir una solicitud para ser aprobada y en qué situaciones debe ser rechazada?

Proponer un requerimiento mejorado.

* El sistema deberá permitir el inicio de sesión mediante correo institucional y contraseña. Solo los usuarios registrados y habilitados podrán acceder. Tras autenticarse, el sistema deberá restringir las funcionalidades disponibles según el rol del usuario: solicitante o encargado.

## Definir reglas de negocio, alcance y exclusiones.

### Reglas de negocio

* **RN-01:** Solo los usuarios registrados y habilitados podrán solicitar préstamos o reservas.
* **RN-02:** Un usuario podrá mantener un máximo de 3 equipos reservados o prestados simultáneamente.
* **RN-03:** Un equipo solo podrá ser reservado si se encuentra disponible durante todo el período solicitado.
* **RN-04:** Dos solicitudes aprobadas no podrán reservar el mismo equipo en períodos de tiempo que se superpongan.
* **RN-05:** Toda solicitud deberá ser aprobada o rechazada por un encargado antes de realizar la entrega.
* **RN-06:** Solo un encargado podrá registrar la entrega y devolución de un equipo.
* **RN-07:** Un préstamo será considerado atrasado cuando haya superado su fecha de devolución sin que esta haya sido registrada.
* **RN-08:** Un usuario que mantenga un préstamo atrasado no podrá realizar nuevas solicitudes hasta devolver los equipos pendientes.
* **RN-09:** Las operaciones sobre un préstamo solo podrán realizar transiciones de estado previamente definidas.
* **RN-10:** Las funcionalidades disponibles estarán restringidas según el rol del usuario autenticado.

### Alcance

El sistema permitirá:

* Registrar y administrar usuarios autorizados.
* Registrar y consultar equipos.
* Autenticar usuarios.
* Crear solicitudes de reserva o préstamo.
* Aprobar y rechazar solicitudes.
* Registrar entregas, devoluciones y cancelaciones.
* Consultar préstamos vigentes, futuros y atrasados.
* Determinar la disponibilidad de los equipos.
* Registrar eventos relevantes mediante logs.
* Manejar entradas inválidas y errores durante las operaciones.

### Exclusiones

El sistema no contemplará:

* Cobro o procesamiento de multas monetarias.
* Pagos en línea.
* Envío automático de correos electrónicos o mensajes de WhatsApp.
* Integración con sistemas externos de la universidad.
* Recuperación automática de contraseñas.
* Aplicación web o interfaz gráfica.
* Gestión de reparación o mantenimiento de equipos.
* Gestión de inventario distinta de los equipos destinados a préstamos.

Establecer criterios de aceptación verificables.

## Criterios de aceptación

* **CA-01: Inicio de sesión:** Dado un usuario registrado y habilitado, cuando ingrese credenciales correctas, el sistema deberá permitirle iniciar sesión y acceder únicamente a las funcionalidades correspondientes a su rol.

* **CA-02: Credenciales incorrectas:** Cuando un usuario ingrese credenciales incorrectas, el sistema deberá rechazar el inicio de sesión y no permitir acceso a las funcionalidades del sistema.

* **CA-03: Límite de equipos:** Si un usuario ya posee 3 equipos reservados o prestados, el sistema deberá rechazar cualquier nueva solicitud que supere dicho límite.

* **CA-04: Disponibilidad:** El sistema deberá rechazar una solicitud cuando alguno de los equipos solicitados ya se encuentre reservado o prestado durante un período que se superponga con el solicitado.

* **CA-05: Aprobación:** Una solicitud pendiente solo podrá ser aprobada o rechazada por un usuario con rol de encargado.

* **CA-06: Entrega:** El sistema solo deberá permitir registrar la entrega de una solicitud previamente aprobada.

* **CA-07: Devolución:** El sistema solo deberá permitir registrar la devolución de un préstamo que haya sido previamente entregado.

* **CA-08: Préstamo atrasado:** Si la fecha de devolución establecida ha sido superada y el equipo no ha sido devuelto, el sistema deberá identificar el préstamo como atrasado.

* **CA-09: Usuario con atraso:** Si un usuario posee al menos un préstamo atrasado, el sistema deberá rechazar una nueva solicitud de préstamo o reserva.

* **CA-10: Transiciones:** El sistema deberá rechazar cualquier intento de realizar una transición de estado que no esté definida como válida.

* **CA-11: Persistencia:** Después de cerrar y volver a ejecutar la aplicación, los usuarios, equipos y préstamos registrados deberán conservarse.

* **CA-12: Entradas inválidas:** Ante una entrada inválida, el sistema deberá rechazar la operación sin modificar los datos existentes ni finalizar inesperadamente.

2.3 Verificación y validación
Explicar, aplicado al proyecto, la diferencia entre:

Verificación: ¿Estamos construyendo correctamente el producto especificado?
Validación: ¿Estamos construyendo el producto que realmente se necesita?
Definir y ejecutar al menos:

5 actividades de verificación.
5 actividades de validación.
Para cada actividad indicar su objetivo, responsable, evidencia, resultado y conclusión. Como se vió en clases "No se aceptarán definiciones únicamente teóricas".