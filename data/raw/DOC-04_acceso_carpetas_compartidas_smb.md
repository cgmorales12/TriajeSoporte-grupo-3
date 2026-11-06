# DOC-04: Mapeo y Diagnóstico de Carpetas Compartidas en Servidor de Archivos (SMB/NAS)

**Categoría:** Carpetas Compartidas  
**Origen:** Departamento de TI — InnovaServicios PYME  
**Vigencia:** 2026 (Almacenamiento Corporativo Centralizado)  
**URL:** https://soporte.pyme-innovaservicios.com/manuales/DOC-04_acceso_carpetas_compartidas_smb.md

## Descripción General
Procedimiento para la conexión, mapeo de unidades de red y solución de problemas de acceso al servidor central de archivos (File Server / NAS) de la PYME.

## Procedimiento Operativo Paso a Paso

### Paso 1: Mapeo de la Unidad de Red en Windows
1. Abra el Explorador de Archivos y haga clic en «Este equipo».
2. En la barra superior, seleccione los tres puntos (...) o la pestaña Equipo y elija «Conectar a unidad de red».
3. En Unidad, elija la letra correspondiente según el departamento:
   - Unidad Z: -> Carpeta General y Procedimientos (\\192.168.10.15\General)
   - Unidad Y: -> Carpeta Departamental Privada (\\192.168.10.15\Contabilidad o Ventas)
4. Marque la casilla «Volver a conectar al iniciar sesión».

### Paso 2: Solución de Error «Acceso Denegado» o «Permisos Insuficientes»
1. Si al hacer doble clic recibe el mensaje «Windows no puede tener acceso... permisos insuficientes», verifique que esté autenticado con su usuario de dominio corporativo y no con una cuenta local.
2. La solicitud de acceso a carpetas de otros departamentos requiere autorización por correo del Jefe de Área.
3. Una vez aprobada, el técnico de TI agrega la cuenta al grupo de seguridad respectivo en Active Directory.

### Paso 3: Pérdida de Conexión tras Suspensión del Equipo
Si la unidad de red aparece con una «X» roja al encender la computadora:
1. Haga doble clic sobre la unidad para forzar la reconexión con el servidor.
2. Si no reconecta, verifique que el cable de red esté conectado o que la VPN esté activa si se encuentra en teletrabajo.
3. Abra la consola cmd y ejecute: 
et use Z: /delete y luego 
et use Z: \\192.168.10.15\General /persistent:yes.

### Paso 4: Política de Capacidad y Prohibición de Archivos Personales
El servidor de archivos cuenta con cuotas de almacenamiento de 50 GB por departamento. Queda estrictamente prohibido guardar copias de películas, música o archivos personales no relacionados con la actividad laboral de la PYME.
