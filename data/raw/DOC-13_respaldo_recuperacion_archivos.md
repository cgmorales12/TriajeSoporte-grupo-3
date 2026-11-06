# DOC-13: Política y Procedimiento de Respaldo y Recuperación de Archivos de Trabajo

**Categoría:** Políticas y Almacenamiento  
**Origen:** Departamento de TI — InnovaServicios PYME  
**Vigencia:** 2026 (Continuidad Operativa y Respaldo de Datos)  
**URL:** https://soporte.pyme-innovaservicios.com/manuales/DOC-13_respaldo_recuperacion_archivos.md

## Descripción General
Directrices para asegurar que la información generada por los 60 colaboradores cuente con copias de respaldo automáticas y procedimiento para la recuperación de archivos sobrescritos o borrados por error.

## Procedimiento Operativo Paso a Paso

### Paso 1: Almacenamiento Exclusivo en Unidades Respaldadas
1. Todo documento de trabajo debe guardarse en la carpeta compartida departamental (Unidad Z: o Y:) o en la carpeta OneDrive corporativa sincronizada.
2. Los archivos guardados en el Escritorio local o en la carpeta Descargas de la computadora NO forman parte de los respaldos automáticos de la empresa.

### Paso 2: Recuperación de Versiones Anteriores (Historial de Archivos)
Si un colaborador modificó un archivo Excel o Word y necesita recuperar el estado de horas antes:
1. Haga clic derecho sobre el archivo en el Explorador de Windows.
2. Seleccione «Propiedades» y vaya a la pestaña «Versiones anteriores».
3. Seleccione el punto de restauración con la fecha y hora deseada y haga clic en «Restaurar».

### Paso 3: Recuperación de Archivos Borrados en Servidor de Red
1. En las carpetas compartidas de red, los archivos borrados no van a la papelera local de la computadora.
2. El servidor de archivos toma instantáneas automáticas (VSS Shadow Copies) cada 4 horas (08:00, 12:00, 16:00 y 20:00).
3. Haga clic derecho sobre la carpeta contenedora -> «Propiedades» -> «Versiones anteriores» y abra la copia previa para recuperar el documento borrado.

### Paso 4: Respaldo Completo Nocturno y Almacenamiento Fuera de Sitio
El servidor central ejecuta un respaldo completo diario a las 23:00 hacia un repositorio NAS aislado y una réplica cifrada en la nube para garantizar continuidad del negocio ante desastres.
