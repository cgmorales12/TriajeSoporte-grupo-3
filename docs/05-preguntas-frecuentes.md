# Levantamiento Real de Información: Preguntas Frecuentes de Soporte Técnico para PYMEs
**Proyecto:** TecnoAula — Triaje Automático de Solicitudes de Soporte Tecnológico para PYMEs (Caso N.º 03 · Grupo 3 UNIANDES)  
**Objetivo:** Consolidado de 15 incidencias y consultas tecnológicas cotidianas recopiladas en entornos corporativos ofimáticos de Pequeñas y Medianas Empresas (50 a 100 colaboradores).

---

## 1. Consolidado de Consultas Frecuentes de Soporte en PYMEs (15 Casos)

| N.º | Consulta / Incidencia Reportada por el Colaborador | Categoría ITIL | Impacto | Urgencia | Procedimiento Técnico RAG Asociado |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **01** | *"Olvidé mi contraseña de Windows y tras 5 intentos fallidos mi cuenta en Active Directory aparece bloqueada."* | Accesos y Contraseñas | Medio | Alta | **DOC-01** (Desbloqueo de cuenta y clave temporal de auto-restablecimiento) |
| **02** | *"Estoy en teletrabajo y el cliente VPN FortiClient se queda colgado en 48% con error de negociación del túnel."* | Redes y Conectividad | Medio | Alta | **DOC-02** (Validación de gateway remoto `vpn.empresa.com`, puerto 443 y token 2FA) |
| **03** | *"La impresora departamental de Administración tiene la luz naranja intermitente y marca atasco de papel en la bandeja 2."* | Hardware y Periféricos | Medio | Media | **DOC-03** (Retiro manual de papel atascado en rodillos y reinicio del spooler de impresión) |
| **04** | *"No puedo acceder a la carpeta compartida en la unidad Z: del servidor de archivos, me sale 'Acceso Denegado'."* | Almacenamiento y Archivos | Medio | Media | **DOC-04** (Verificación de pertenencia a grupo de seguridad SMB y comando `net use`) |
| **05** | *"Al ingresar al sistema contable / ERP me sale el error 'Usuario ya tiene una sesión activa en otra estación'."* | Software Corporativo | Alto | Alta | **DOC-05** (Finalización de proceso bloqueado en el servidor transaccional y validación SRI) |
| **06** | *"Recibí un correo sospechoso con un archivo .zip solicitando datos bancarios, ¿qué debo hacer?"* | Seguridad de la Información | Alto | Alta | **DOC-06** (Política ISO 27002: aislamiento de phishing y reporte inmediato a seguridad TI) |
| **07** | *"Mi computadora de escritorio se quedó sin internet y los LEDs del puerto Ethernet de la pared no encienden."* | Redes y Conectividad | Medio | Media | **DOC-07** (Inspección física de cable UTP, conector RJ-45 y verificación de switch de piso) |
| **08** | *"Cambié de smartphone corporativo y no puedo conectar a la red Wi-Fi de la oficina."* | Redes Inalámbricas | Bajo | Baja | **DOC-08** (Selección de Red-Corporativa-Segura, autenticación WPA2-Enterprise y certificado) |
| **09** | *"El antivirus Microsoft Defender muestra una alerta de amenaza de malware detectada en la carpeta de descargas."* | Ciberseguridad Endpoint | Alto | Alta | **DOC-09** (Aislamiento en cuarentena, análisis completo del equipo y actualización de firmas) |
| **10** | *"Mi laptop de trabajo se congeló súbitamente mostrando una pantalla azul (BSOD) y emite un ruido metálico."* | Soporte a Estaciones | Alto | Alta | **DOC-10** (Detección de fallo crítico de disco; escalamiento a soporte presencial Nivel 2) |
| **11** | *"Outlook no envía ni recibe correos porque me notifica que el buzón de almacenamiento superó los 50 GB."* | Correo y Colaboración | Medio | Media | **DOC-11** (Vaciado de elementos eliminados y autoarchivado de mensajes antiguos en archivo PST) |
| **12** | *"El lunes se incorpora un nuevo colaborador en Ventas y necesitamos crear su usuario, correo y permisos."* | Identidad y Accesos | Bajo | Media | **DOC-12** (Procedimiento formal de alta en Active Directory y licenciamiento ofimático) |
| **13** | *"Borré por error una hoja de cálculo compartida en la que trabajé toda la mañana, ¿cómo puedo recuperarla?"* | Respaldo y Continuidad | Medio | Alta | **DOC-13** (Recuperación mediante versiones anteriores de Windows Server - Shadow Copies VSS) |
| **14** | *"Conecté un segundo monitor mediante cable HDMI al docking station de mi laptop pero no detecta señal."* | Hardware de Oficina | Bajo | Baja | **DOC-14** (Atajo `Win + P` para extender escritorio y ajuste de resolución en Configuración) |
| **15** | *"¿Cuál es el tiempo máximo de atención (SLA) si se cae el servidor de facturación a fin de mes?"* | Gestión de Incidentes | Alto | Alta | **DOC-15** (Consulta de Matriz ITIL: Prioridad Alta, tiempo de respuesta SLA $\le 15$ minutos) |

---

## 2. Conclusiones para el Modelo de Triaje
1. **Alta Tasa de Autoatención Nivel 1 ($\ge 70\%$):** Las consultas 1, 2, 3, 4, 7, 8, 11, 13 y 14 pueden ser resueltas por el propio colaborador siguiendo las guías paso a paso del RAG, liberando al técnico de TI.
2. **Escalamiento Obligatorio a Nivel 2:** Las incidencias 5, 10 y 12 requieren intervención física del técnico o privilegios de administrador de dominio.
3. **Seguridad y LOPDP:** Casos como el 1 y el 6 exigen blindaje de contraseñas y detección de phishing según la política ISO 27002.
