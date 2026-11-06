# DOC-07: Diagnóstico y Solución de Conexión a Internet y Red Cableada en Oficina

**Categoría:** Red y Conectividad  
**Origen:** Departamento de TI — InnovaServicios PYME  
**Vigencia:** 2026 (Infraestructura de Red LAN Corporativa)  
**URL:** https://soporte.pyme-innovaservicios.com/manuales/DOC-07_conectividad_red_cableada_oficina.md

## Descripción General
Procedimiento para la resolución de caídas de enlace, lentitud y desconexión en las estaciones de trabajo conectadas mediante cable de red Ethernet a los switches de distribución de la oficina.

## Procedimiento Operativo Paso a Paso

### Paso 1: Inspección Física del Cable UTP y Roseta
1. Verifique que el conector RJ-45 esté firmemente insertado en la tarjeta de red de la PC y en la toma de pared (roseta).
2. Compruebe que el LED de enlace (LINK/ACT) parpadee en color verde o naranja. Si el LED está completamente apagado, pruebe con un cable de red de repuesto disponible en el armario de piso.

### Paso 2: Liberación y Renovación de Dirección IP (DHCP)
Si el icono de red en la barra de tareas muestra un signo de exclamación o «Sin acceso a internet»:
1. Presione Win + R, escriba cmd y presione Enter.
2. Escriba ipconfig /release y presione Enter para liberar la asignación anterior.
3. Escriba ipconfig /renew para solicitar una nueva dirección IP al servidor DHCP de la oficina.

### Paso 3: Diagnóstico de Puerta de Enlace y DNS Corporativo
1. En la misma consola cmd, ejecute: ping 192.168.10.1 (puerta de enlace predeterminada / firewall).
2. Si responde correctamente, ejecute: ping 8.8.8.8 para comprobar salida hacia internet.
3. Si solo navega por IP pero no por nombre, vacíe la caché de resolución ejecutando ipconfig /flushdns.

### Paso 4: Escalamiento por Falla Masiva de Switch de Piso
Si más de 5 colaboradores del mismo departamento pierden la conexión simultáneamente, no se trata de una falla individual. El agente clasifica el incidente con Prioridad Alta y asigna ticket urgente al técnico de TI para revisión física del switch en el rack de comunicaciones.
