# DOC-08: Conexión Segura al Wi-Fi Corporativo de la Oficina y Red de Visitas

**Categoría:** Red y Conectividad  
**Origen:** Departamento de TI — Mesa de Ayuda TI — Estándar Operativo PYME  
**Vigencia:** 2026 (Redes Inalámbricas Seguras WPA3/WPA2-Enterprise)  
**URL:** https://soporte.pyme-estandar.org/manuales/DOC-08_wifi_corporativo_credenciales.md

## Descripción General
Instrucciones para la conexión de computadoras portátiles corporativas y dispositivos móviles autorizados a la red inalámbrica de la empresa.

## Procedimiento Operativo Paso a Paso

### Paso 1: Selección de la Red Inalámbrica Corporativa
1. En la barra de tareas de Windows, haga clic en el icono de red Wi-Fi.
2. Localice y seleccione la red Red-Corporativa-Segura (no utilice redes abiertas ni de locales vecinos).
3. Asegúrese de tener marcada la opción «Conectarse automáticamente cuando esté en el alcance».

### Paso 2: Autenticación con Credenciales de Dominio
1. Cuando el sistema lo solicite, ingrese su usuario y contraseña corporativa de Windows.
2. Si aparece una advertencia de seguridad indicando «¿Desea continuar conectándose al certificado de servidor?», verifique que el servidor sea 
adius.empresa.com y haga clic en «Conectar».

### Paso 3: Solución de Error «No se puede conectar a esta red»
1. Abra Configuración de Windows -> Red e Internet -> Wi-Fi -> Administrar redes conocidas.
2. Localice Red-Corporativa-Segura y haga clic en «Dejar de recordar».
3. Reinicie el adaptador inalámbrico apagando y encendiendo el Wi-Fi, y vuelva a conectarse ingresando sus credenciales actualizadas.

### Paso 4: Red de Invitados para Clientes y Proveedores Externos
Para personas externas que visitan la oficina:
1. Deben conectarse exclusivamente a la red abierta Red-Invitados-Visitas.
2. Esta red cuenta con aislamiento de clientes (Client Isolation) y solo permite navegación web hacia internet, sin acceso a servidores ni impresoras de la PYME.
