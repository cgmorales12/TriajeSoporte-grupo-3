# DOC-02: Guía de Conexión y Configuración de VPN Corporativa para Teletrabajo

**Categoría:** Red y VPN  
**Origen:** Departamento de TI — InnovaServicios PYME  
**Vigencia:** 2026 (Teletrabajo y Acceso Remoto Seguro)  
**URL:** https://soporte.pyme-innovaservicios.com/manuales/DOC-02_configuracion_vpn_corporativa.md

## Descripción General
Instrucciones oficiales para colaboradores en modalidad de teletrabajo que requieren acceder a los servidores locales, carpetas compartidas y sistema contable de la empresa mediante túnel cifrado SSL-VPN.

## Procedimiento Operativo Paso a Paso

### Paso 1: Verificación del Cliente VPN Instalado
1. Compruebe que en su equipo portátil corporativo se encuentre instalado el software oficial FortiClient VPN o cliente OpenVPN institucional.
2. Si la aplicación no está instalada, no intente descargar instaladores de sitios web no autorizados; comuníquelo al técnico de TI para despliegue por repositorio central.

### Paso 2: Parámetros del Servidor y Gateway Remoto
1. Abra el cliente VPN y seleccione la conexión «VPN-Innova-Remoto».
2. Verifique que el campo Gateway remoto contenga: pn.innovaservicios.com y puerto SSL 443 (o 10443).
3. Active la casilla de verificación «Habilitar túnel seguro con cifrado AES-256».

### Paso 3: Autenticación de Usuario y Doble Factor (2FA)
1. Ingrese su usuario institucional (sin agregar @dominio) y su contraseña de red.
2. Al pulsar Conectar, el sistema solicitará el código de verificación temporal (Token OTP).
3. Abra la aplicación de autenticación en su teléfono móvil corporativo e ingrese el código de 6 dígitos antes de que expire el temporizador (30 segundos).

### Paso 4: Comprobación de Enlace y Resolución de Nombres
1. Una vez alcanzado el 100% de conexión, el estado cambiará a «Conectado» con una IP asignada del rango 192.168.50.X.
2. Abra la consola de comandos (cmd) y ejecute ping 192.168.10.5 para comprobar comunicación con el servidor central de archivos.
3. Si la conexión falla con código de error de credenciales inválidas, verifique que la tecla Bloq Mayús no esté activa.
