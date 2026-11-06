# DOC-05: Manual de Usuario y Solución de Bloqueos en el Sistema Contable / ERP Interno

**Categoría:** Sistema Contable y Software  
**Origen:** Departamento de TI — InnovaServicios PYME  
**Vigencia:** 2026 (Facturación Electrónica y ERP)  
**URL:** https://soporte.pyme-innovaservicios.com/manuales/DOC-05_sistema_contable_erp.md

## Descripción General
Guía de soporte para resolver incidencias operativas, bloqueos de concurrencia y errores de timbrado en el sistema contable corporativo utilizado por los departamentos administrativo y financiero.

## Procedimiento Operativo Paso a Paso

### Paso 1: Error «Usuario ya tiene una sesión activa en otra estación»
Este error ocurre cuando el colaborador cerró bruscamente la aplicación o hubo una microdesconexión de red:
1. Solicite al técnico de TI el reinicio de la sesión huérfana en la consola del ERP.
2. El técnico ingresa al módulo de Monitoreo de Sesiones del ERP y pulsa «Finalizar sesión colgada» para el ID de usuario afectado.
3. El colaborador espera 60 segundos y vuelve a iniciar sesión con normalidad.

### Paso 2: Error de Conexión con el Motor de Base de Datos SQL
Si al abrir el sistema contable aparece «Error 10061: No se puede conectar con el servidor SQL 192.168.10.20:
1. Verifique que la computadora tenga conexión a la red de la oficina (puerto cableado o VPN activa).
2. Compruebe que el servicio SQL Server Browser esté respondiendo en el puerto 1433.
3. Si el error es masivo para todo el departamento contable, clasifique el incidente con Impacto Alto y Urgencia Alta para atención inmediata del técnico de TI.

### Paso 3: Falla de Timbrado y Firma Electrónica de Comprobantes
1. Compruebe la vigencia del certificado digital de firma electrónica en formato .p12 o .pfx.
2. Verifique la conectividad con los servicios web del SRI (Servicio de Rentas Internas) ingresando al portal oficial.
3. Si el certificado expiró, se debe notificar a Contabilidad para la renovación de la firma digital con el proveedor autorizado.

### Paso 4: Limpieza de Archivos Temporales y Caché del ERP
Si el sistema contable presenta lentitud al calcular balances o emitir facturas:
1. Cierre el sistema contable por completo.
2. Abra Win + R, escriba %temp% y elimine los archivos temporales de sesión.
3. Ejecute el acceso directo «Reparar Caché ERP» ubicado en el escritorio corporativo.
