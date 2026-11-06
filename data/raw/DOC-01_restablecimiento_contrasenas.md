# DOC-01: Procedimiento para Restablecimiento de Contraseñas de Dominio Windows y Correo Corporativo

**Categoría:** Accesos y Contraseñas  
**Origen:** Departamento de Tecnologías de la Información (TI) — Mesa de Ayuda TI — Estándar Operativo PYME  
**Vigencia:** 2026 (Norma ISO/IEC 27002)  
**URL:** https://soporte.pyme-estandar.org/manuales/DOC-01_restablecimiento_contrasenas.md

## Descripción General
Procedimiento estándar para el desbloqueo de cuentas y restablecimiento de contraseñas de red en Active Directory y cliente de correo corporativo para los colaboradores de la empresa (entorno corporativo PYME).

## Procedimiento Operativo Paso a Paso

### Paso 1: Verificación de Identidad del Colaborador
Por políticas de seguridad estricta y cumplimiento LOPDP, el sistema de triaje o el técnico de TI NUNCA debe solicitar ni almacenar la contraseña actual del colaborador. Se verifica únicamente el nombre completo, cargo y correo institucional corporativo.

### Paso 2: Desbloqueo de Cuenta Bloqueada por Intentos Fallidos
Si el colaborador ingresó erróneamente su clave más de 5 veces consecutivas, la directiva de seguridad bloquea la cuenta durante 30 minutos:
1. El técnico de TI accede a la consola de usuarios de Active Directory.
2. Localiza la cuenta del usuario y marca la opción «Desbloquear la cuenta».
3. Si el usuario recuerda su clave, puede intentar el inicio de sesión inmediatamente tras el desbloqueo.

### Paso 3: Asignación de Contraseña Temporal de Auto-Restablecimiento
En caso de olvido definitivo de la credencial:
1. El técnico genera una contraseña temporal de alta entropía (mínimo 12 caracteres, al menos una mayúscula, un número y un símbolo).
2. Se activa obligatoriamente la casilla «El usuario debe cambiar la contraseña en el siguiente inicio de sesión».
3. Se remite la clave temporal por canal alternativo seguro y verificado.

### Paso 4: Sincronización de Contraseña en Dispositivos y Correo
Tras actualizar la clave de Windows en la estación de trabajo:
1. Bloquear y desbloquear la sesión (Win + L) para refrescar el ticket Kerberos.
2. Abrir Microsoft Outlook y colocar la nueva contraseña cuando aparezca el diálogo de autenticación.
3. Actualizar la clave en la red Wi-Fi corporativa y en la VPN del equipo portátil.
