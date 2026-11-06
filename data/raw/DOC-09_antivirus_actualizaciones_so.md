# DOC-09: Protocolo de Actualización de Windows y Antivirus Corporativo en Estaciones

**Categoría:** Software y Seguridad  
**Origen:** Departamento de TI — Mesa de Ayuda TI — Estándar Operativo PYME  
**Vigencia:** 2026 (Mantenimiento de Endpoint Security)  
**URL:** https://soporte.pyme-estandar.org/manuales/DOC-09_antivirus_actualizaciones_so.md

## Descripción General
Procedimiento para la supervisión del estado del antivirus corporativo, ejecución de escaneos preventivos y aplicación de parches críticos del sistema operativo en las 60 estaciones de la empresa.

## Procedimiento Operativo Paso a Paso

### Paso 1: Verificación de Estado del Antivirus Corporativo
1. En el área de notificaciones (esquina inferior derecha), compruebe que el icono del antivirus corporativo (Endpoint Protection) se encuentre con el escudo en color verde.
2. Si el icono muestra un triángulo amarillo o rojo, haga doble clic y presione «Actualizar definiciones de firmas ahora».

### Paso 2: Ejecución de Análisis Rápido ante Comportamiento Anómalo
Si el equipo presenta apertura espontánea de ventanas de publicidad o lentitud extrema:
1. Abra el antivirus corporativo y seleccione «Análisis rápido».
2. El análisis tomará entre 3 y 8 minutos. Si detecta amenazas en cuarentena, no intente restaurarlas manualmente; el técnico de TI recibe la alerta en la consola central.

### Paso 3: Instalación de Parches Críticos de Windows Update
1. Abra Inicio -> Configuración -> Windows Update.
2. Haga clic en «Buscar actualizaciones».
3. Las actualizaciones que requieren reinicio deben programarse al finalizar la jornada laboral (18:00) para no interrumpir las actividades de la oficina.

### Paso 4: Aislamiento Preventivo de Red ante Detección de Ransomware
Si un colaborador observa que sus archivos cambian de extensión o aparece una nota de rescate en pantalla:
1. Desconecte inmediatamente el cable de red Ethernet de la pared y apague el Wi-Fi del equipo.
2. Apague la computadora manteniendo presionado el botón de encendido por 10 segundos.
3. Notifique de forma presencial o por llamada telefónica de urgencia máxima al técnico de TI para contener la propagación.
