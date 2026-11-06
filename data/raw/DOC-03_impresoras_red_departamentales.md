# DOC-03: Guía de Conexión y Solución de Problemas en Impresoras Multifunción de Red

**Categoría:** Impresoras y Periféricos  
**Origen:** Departamento de TI — Mesa de Ayuda TI — Estándar Operativo PYME  
**Vigencia:** 2026 (Equipamiento Ofimático Departamental)  
**URL:** https://soporte.pyme-estandar.org/manuales/DOC-03_impresoras_red_departamentales.md

## Descripción General
Manual técnico para la agregación, configuración de controladores y resolución de incidencias en las impresoras multifunción láser conectadas a la red local de la empresa.

## Procedimiento Operativo Paso a Paso

### Paso 1: Conexión a la Impresora de su Departamento por IP
1. Presione las teclas Win + R, escriba control printers y presione Enter.
2. Haga clic en «Agregar una impresora» y elija «La impresora que deseo no está en la lista».
3. Seleccione «Agregar una impresora por medio de una dirección TCP/IP» y coloque la IP de su departamento:
   - Impresora Contabilidad y Finanzas: 192.168.10.40
   - Impresora Ventas y Operaciones: 192.168.10.41
   - Impresora Gerencia y RRHH: 192.168.10.42

### Paso 2: Instalación del Controlador PCL6 Certificado
1. Seleccione el controlador preinstalado «HP LaserJet Pro / Ricoh Universal PCL6».
2. No modifique los parámetros de puerto RAW ni la cola 9100.
3. Establezca la impresora como predeterminada según las necesidades de su puesto de trabajo.

### Paso 3: Desatasco de la Cola de Impresión de Windows
Si los documentos se quedan en estado «Imprimiendo» o «Error»:
1. Presione Win + R, escriba services.msc y presione Enter.
2. Busque el servicio llamado «Cola de impresión» (Print Spooler), haga clic derecho y seleccione «Detener».
3. Abra el explorador de archivos y borre todos los archivos dentro de C:\Windows\System32\spool\PRINTERS.
4. Regrese a la ventana de servicios y haga clic derecho en «Cola de impresión» -> «Iniciar».

### Paso 4: Falla de Hardware Físico (Atasco de Papel o Tóner)
Si la pantalla del equipo multifunción muestra «Atasco en bandeja 2» o «Tóner negro agotado», este incidente requiere intervención física. El agente de triaje debe crear un ticket asignado al técnico de TI para reposición de insumos o retiro del papel atascado.
