"""
Script para configurar exactamente 5 tickets didácticos y diversos en cada columna del Kanban:
- 5 en Nuevos (nuevo): Autoatención N1 + Regla de silencio
- 5 en En Atención (en_atencion): Soporte Remoto TI / NOC / ERP
- 5 en Escalado a Soporte Presencial (escalado_cuadrilla): Nivel 3 Hardware y Red Física
- 5 en Resueltos (resuelto): Validación y Cierre Satisfactorio de SLA

Todos con citas RAG verificables a los 15 manuales técnicos oficiales de Soporte Microinformático para PYMEs.
Redactados con respuestas claras, empáticas y orientadas al usuario no técnico.
"""

import sqlite3
import os
import sys
import json
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "conectatec.db")

TICKETS_PYME = [
    # =========================================================================
    # 1. NUEVOS (nuevo) · 5 Tickets: Nivel 1 Autoatención / Entrada
    # =========================================================================
    {
        "codigo": "TCK-N01-AD",
        "estado": "nuevo",
        "cliente": "Ana Martínez (Contabilidad - Puesto 04)",
        "email": "ana.martinez@empresa.com",
        "problema": "Mi cuenta de usuario en Active Directory se bloqueó después de ingresar 3 veces la clave equivocada y no puedo acceder al correo corporativo ni al equipo.",
        "categoria": "Accesos y Contraseñas",
        "impacto": "Bajo",
        "urgencia": "Alta",
        "prioridad": "Media",
        "sla": 120,
        "desc_sla": "Atención técnica en menos de 2 horas (SLA Matriz ITIL)",
        "solucion": "1. Verifique su identidad con el técnico de soporte.\n2. El técnico reactivará su usuario en el sistema.\n3. Inicie sesión con la clave temporal y cree una contraseña personal nueva de al menos 12 caracteres.",
        "citas": [{
            "documento_id": "DOC-01_restablecimiento_contrasenas.md",
            "titulo_documento": "Procedimiento para Restablecimiento de Contraseñas de Dominio Windows y Correo Corporativo",
            "paso_exacto": "Paso 2: Desbloqueo de Cuenta en Active Directory",
            "fragmento_aplicado": "«Su cuenta se bloqueó por seguridad tras varios intentos. Para reactivarla, un técnico validará su identidad y le entregará una clave provisional para que cree su nueva contraseña.»",
            "url": "https://soporte.pyme-estandar.org/manuales/DOC-01_restablecimiento_contrasenas.md"
        }],
        "modo_vuln": 0,
        "aluc_det": 0,
        "proveedor": "gemini",
        "tokens": 412,
        "justif": "Solicitud individual de desbloqueo de credenciales en dominio Active Directory. Clasificación estándar Nivel 1 según DOC-01."
    },
    {
        "codigo": "TCK-N02-VPN",
        "estado": "nuevo",
        "cliente": "Carlos Viteri (Ventas - Teletrabajo)",
        "email": "carlos.viteri@empresa.com",
        "problema": "El cliente FortiClient VPN se queda en 48% con error de negociación TLS y no me permite conectar desde mi casa a los archivos compartidos de la empresa.",
        "categoria": "Red y VPN",
        "impacto": "Bajo",
        "urgencia": "Alta",
        "prioridad": "Media",
        "sla": 120,
        "desc_sla": "Atención técnica en menos de 2 horas (SLA Matriz ITIL)",
        "solucion": "1. Cierre FortiClient completamente y vuelva a abrirlo.\n2. Verifique que la dirección sea vpn.empresa.com:10443.\n3. Si el error persiste, un técnico le instalará de forma remota el certificado de seguridad de la empresa.",
        "citas": [{
            "documento_id": "DOC-02_configuracion_vpn_corporativa.md",
            "titulo_documento": "Guía de Conexión y Configuración de VPN Corporativa para Teletrabajo",
            "paso_exacto": "Paso 3: Verificación de Parámetros TLS y Certificados",
            "fragmento_aplicado": "«La conexión VPN se detuvo por falta del certificado de seguridad de la empresa. Reinicie el programa FortiClient o solicite al técnico la instalación del certificado para teletrabajo.»",
            "url": "https://soporte.pyme-estandar.org/manuales/DOC-02_configuracion_vpn_corporativa.md"
        }],
        "modo_vuln": 0,
        "aluc_det": 0,
        "proveedor": "gemini",
        "tokens": 448,
        "justif": "Incidencia de acceso remoto seguro para teletrabajo. Diagnóstico según protocolo de VPN corporativa DOC-02."
    },
    {
        "codigo": "TCK-N03-WIFI",
        "estado": "nuevo",
        "cliente": "Sofía Delgado (Recepción y Logística)",
        "email": "sofia.delgado@empresa.com",
        "problema": "Mi laptop institucional se desconecta intermitentemente del Wi-Fi corporativo 'PYME-CORP-5G' y me solicita volver a escribir el usuario de red cada media hora.",
        "categoria": "Red y Conectividad",
        "impacto": "Bajo",
        "urgencia": "Baja",
        "prioridad": "Baja",
        "sla": 1440,
        "desc_sla": "Atención en jornada laboral / Autoatención guiada en 24 horas",
        "solucion": "1. Haga clic en el ícono de Wi-Fi, clic derecho en 'PYME-CORP-5G' y elija 'Olvidar'.\n2. Vuelva a conectarse escribiendo su usuario de red corporativo y contraseña.\n3. Cuando Windows le pregunte si confía en la red, presione 'Conectar' para guardar la clave.",
        "citas": [{
            "documento_id": "DOC-08_wifi_corporativo_credenciales.md",
            "titulo_documento": "Conexión Segura al Wi-Fi Corporativo de la Oficina y Red de Visitas",
            "paso_exacto": "Paso 2: Validación de Certificado WPA2-Enterprise y Credenciales",
            "fragmento_aplicado": "«En la lista de redes Wi-Fi, seleccione 'Olvidar red' en 'PYME-CORP-5G' y vuelva a conectarse ingresando su usuario y clave corporativa aceptando el certificado de seguridad.»",
            "url": "https://soporte.pyme-estandar.org/manuales/DOC-08_wifi_corporativo_credenciales.md"
        }],
        "modo_vuln": 0,
        "aluc_det": 0,
        "proveedor": "gemini",
        "tokens": 395,
        "justif": "Problema de reconexión inalámbrica individual en el puesto de trabajo. Aplicación de procedimiento de red DOC-08."
    },
    {
        "codigo": "TCK-N04-MAIL",
        "estado": "nuevo",
        "cliente": "Gabriel Ochoa (Compras y Proveedores)",
        "email": "gabriel.ochoa@empresa.com",
        "problema": "En Outlook aparece la advertencia 'Buzón de correo al 98% de capacidad' y los correos con cotizaciones de proveedores rebotan indicando cuota excedida.",
        "categoria": "Software y Comunicaciones",
        "impacto": "Bajo",
        "urgencia": "Media",
        "prioridad": "Baja",
        "sla": 480,
        "desc_sla": "Atención en la jornada laboral (8 horas)",
        "solucion": "1. Haga clic derecho en la carpeta 'Elementos eliminados' de Outlook y seleccione 'Vaciar carpeta'.\n2. Revise la carpeta 'Correo no deseado' y elimine los correos innecesarios.\n3. Si requiere ayuda para archivar correos de años anteriores, un técnico le ayudará a moverlos a su equipo local.",
        "citas": [{
            "documento_id": "DOC-11_configuracion_cliente_correo.md",
            "titulo_documento": "Configuración de Cliente de Correo Corporativo, Buzón y Filtro Antispam",
            "paso_exacto": "Paso 3: Depuración y Archivado Local de Mensajes Antiguos",
            "fragmento_aplicado": "«Su buzón está lleno. Vacíe la papelera de Outlook ('Elementos eliminados') y mueva los correos antiguos con archivos adjuntos a una carpeta local de archivo para liberar espacio.»",
            "url": "https://soporte.pyme-estandar.org/manuales/DOC-11_configuracion_cliente_correo.md"
        }],
        "modo_vuln": 0,
        "aluc_det": 0,
        "proveedor": "gemini",
        "tokens": 420,
        "justif": "Gestión de almacenamiento en cliente de correo electrónico. Guía estándar de optimización de buzón DOC-11."
    },
    {
        "codigo": "TCK-N05-SILENCIO",
        "estado": "nuevo",
        "cliente": "David Paredes (Administración General)",
        "email": "david.paredes@empresa.com",
        "problema": "Buenos días, quisiera saber a qué hora entregan el menú del almuerzo hoy en el comedor institucional y si el viernes habrá transporte para la integración.",
        "categoria": "Solicitud No Técnica / Fuera de Alcance",
        "impacto": "Bajo",
        "urgencia": "Baja",
        "prioridad": "Baja",
        "sla": 1440,
        "desc_sla": "Atención regular / Consulta informativa",
        "solucion": "Esta solicitud no describe una avería de computadoras, redes o programas corporativos. Por favor consulte directamente con el departamento de Recursos Humanos o Administración General.",
        "citas": [],
        "modo_vuln": 0,
        "aluc_det": 0,
        "proveedor": "gemini",
        "tokens": 280,
        "justif": "Regla de abstención y silencio institucional: La solicitud es administrativa/social, no técnica. Se aplica tolerancia cero a alucinaciones (0 citas generadas)."
    },

    # =========================================================================
    # 2. EN ATENCIÓN (en_atencion) · 5 Tickets: Soporte Remoto / TI / ERP
    # =========================================================================
    {
        "codigo": "TCK-A01-ERP",
        "estado": "en_atencion",
        "cliente": "Patricia Gómez (Jefa de Contabilidad)",
        "email": "patricia.gomez@empresa.com",
        "problema": "El sistema contable ERP muestra 'Error: Bloqueo de sesión concurrente por usuario desconectado' y no podemos emitir los comprobantes electrónicos del cierre fiscal.",
        "categoria": "Sistema Contable y Software",
        "impacto": "Medio",
        "urgencia": "Alta",
        "prioridad": "Alta",
        "sla": 30,
        "desc_sla": "Atención departamental prioritaria en menos de 30 minutos",
        "solucion": "1. Cierre el programa ERP en su equipo.\n2. Soporte técnico cerrará la sesión colgada en el servidor contable.\n3. En 5 minutos podrá volver a iniciar sesión con normalidad para continuar con la facturación.",
        "citas": [{
            "documento_id": "DOC-05_sistema_contable_erp.md",
            "titulo_documento": "Manual de Usuario y Solución de Bloqueos en el Sistema Contable / ERP Interno",
            "paso_exacto": "Paso 2: Liberación de Sesión Huérfana en el Administrador de Conexiones",
            "fragmento_aplicado": "«Su sesión quedó abierta tras una desconexión. Cierre la ventana del sistema ERP; el equipo de soporte liberará su usuario en el servidor para que pueda ingresar a facturar nuevamente.»",
            "url": "https://soporte.pyme-estandar.org/manuales/DOC-05_sistema_contable_erp.md"
        }],
        "modo_vuln": 0,
        "aluc_det": 0,
        "proveedor": "gemini",
        "tokens": 510,
        "justif": "Afecta a varios colaboradores en proceso contable crítico con vencimiento de cierre. Prioridad Alta con SLA 30m."
    },
    {
        "codigo": "TCK-A02-SMB",
        "estado": "en_atencion",
        "cliente": "Mauricio Paz (Operaciones - Puesto 10)",
        "email": "mauricio.paz@empresa.com",
        "problema": "La unidad de red compartida Z: (Servidor NAS Contable) aparece con una cruz roja indicando 'Ruta de red no encontrada o acceso denegado'.",
        "categoria": "Carpetas Compartidas",
        "impacto": "Medio",
        "urgencia": "Media",
        "prioridad": "Media",
        "sla": 240,
        "desc_sla": "Atención técnica en menos de 4 horas laborables",
        "solucion": "1. Guarde y cierre cualquier archivo abierto.\n2. Cierre sesión en Windows y vuelva a ingresar.\n3. Si la unidad sigue con cruz roja, un técnico verificará sus permisos en el servidor de archivos.",
        "citas": [{
            "documento_id": "DOC-04_acceso_carpetas_compartidas_smb.md",
            "titulo_documento": "Mapeo y Diagnóstico de Carpetas Compartidas en Servidor de Archivos (SMB/NAS)",
            "paso_exacto": "Paso 2: Re-mapeo del Recurso Compartido mediante Script Net Use",
            "fragmento_aplicado": "«La carpeta compartida Z: no responde. Cierre sus documentos, reinicie la sesión de Windows y verifique que su cable de red esté conectado para que el sistema reconecte la unidad compartida.»",
            "url": "https://soporte.pyme-estandar.org/manuales/DOC-04_acceso_carpetas_compartidas_smb.md"
        }],
        "modo_vuln": 0,
        "aluc_det": 0,
        "proveedor": "gemini",
        "tokens": 465,
        "justif": "Dificultad de acceso a archivos compartidos departamentales. Solución lógica en servidor SMB según DOC-04."
    },
    {
        "codigo": "TCK-A03-PRINT",
        "estado": "en_atencion",
        "cliente": "Elena Rivas (Recursos Humanos - Piso 2)",
        "email": "elena.rivas@empresa.com",
        "problema": "La impresora multifunción de red HP LaserJet departamental tiene la cola de impresión bloqueada con 12 trabajos colgados y no deja imprimir contratos laborales.",
        "categoria": "Impresoras y Periféricos",
        "impacto": "Medio",
        "urgencia": "Media",
        "prioridad": "Media",
        "sla": 240,
        "desc_sla": "Atención técnica en menos de 4 horas laborables",
        "solucion": "1. No intente enviar más impresiones para no saturar la máquina.\n2. Soporte técnico cancelará de forma remota el documento trabado.\n3. Una vez limpia la cola, se enviará una página de prueba y podrá imprimir sus contratos.",
        "citas": [{
            "documento_id": "DOC-03_impresoras_red_departamentales.md",
            "titulo_documento": "Guía de Conexión y Solución de Problemas en Impresoras Multifunción de Red",
            "paso_exacto": "Paso 2: Reinicio del Servicio Spooler y Purga de Archivos SPL",
            "fragmento_aplicado": "«La impresora compartida está pausada por un documento trabado. No envíe más impresiones; soporte técnico está reiniciando la cola de impresión de la red para reanudar los trabajos.»",
            "url": "https://soporte.pyme-estandar.org/manuales/DOC-03_impresoras_red_departamentales.md"
        }],
        "modo_vuln": 0,
        "aluc_det": 0,
        "proveedor": "gemini",
        "tokens": 480,
        "justif": "Afecta a impresora compartida de varios colaboradores de RRHH. Prioridad Media con SLA 240m."
    },
    {
        "codigo": "TCK-A04-RED",
        "estado": "en_atencion",
        "cliente": "Fernando Cárdenas (Atención al Cliente)",
        "email": "fernando.cardenas@empresa.com",
        "problema": "El puerto Ethernet de la estación 14 tiene luz ámbar intermitente y el navegador muestra 'DNS_PROBE_FINISHED_NO_INTERNET' al cargar el portal de gestión.",
        "categoria": "Red y Conectividad",
        "impacto": "Bajo",
        "urgencia": "Alta",
        "prioridad": "Media",
        "sla": 120,
        "desc_sla": "Atención técnica en menos de 2 horas",
        "solucion": "1. Verifique que el cable de red detrás de la computadora esté bien encajado (debe hacer 'clic').\n2. Soporte técnico reiniciará la configuración de red de su estación.\n3. Pruebe abrir nuevamente el portal de gestión en el navegador.",
        "citas": [{
            "documento_id": "DOC-07_conectividad_red_cableada_oficina.md",
            "titulo_documento": "Diagnóstico y Solución de Conexión a Internet y Red Cableada en Oficina",
            "paso_exacto": "Paso 2: Liberación de Caché DNS e IP mediante ipconfig",
            "fragmento_aplicado": "«Su equipo no tiene conexión a internet. Desconecte y vuelva a enchufar firmemente el cable de red azul detrás de su computadora; soporte técnico está verificando la señal en el conmutador.»",
            "url": "https://soporte.pyme-estandar.org/manuales/DOC-07_conectividad_red_cableada_oficina.md"
        }],
        "modo_vuln": 0,
        "aluc_det": 0,
        "proveedor": "gemini",
        "tokens": 435,
        "justif": "Fallo de resolución de nombres en equipo individual de atención. Aplicación de protocolo de conectividad DOC-07."
    },
    {
        "codigo": "TCK-A05-FAILOVER",
        "estado": "en_atencion",
        "cliente": "Diego Jácome (Comercial - Puesto 03)",
        "email": "diego.jacome@empresa.com",
        "problema": "Windows Defender emitió una alerta de 'Script no reconocido bloqueado en carpeta temporal' tras descargar un archivo adjunto de correo sospechoso.",
        "categoria": "Software y Seguridad",
        "impacto": "Medio",
        "urgencia": "Alta",
        "prioridad": "Alta",
        "sla": 30,
        "desc_sla": "Atención departamental en menos de 30 minutos",
        "solucion": "1. Desconecte el cable de red o apague el Wi-Fi de su computadora de inmediato.\n2. No abra ni reenvíe el archivo descargado.\n3. Espere al técnico de seguridad informática, quien revisará el equipo para eliminar cualquier amenaza.",
        "citas": [{
            "documento_id": "DOC-09_antivirus_actualizaciones_so.md",
            "titulo_documento": "Protocolo de Actualización de Windows y Antivirus Corporativo en Estaciones",
            "paso_exacto": "Paso 1: Aislamiento Inmediato de Estación y Escaneo Fuera de Línea",
            "fragmento_aplicado": "«Por seguridad, desconecte de inmediato el cable de red o desactive el Wi-Fi de su equipo y no abra el archivo adjunto. Un técnico de seguridad acudirá a revisar la computadora.»",
            "url": "https://soporte.pyme-estandar.org/manuales/DOC-09_antivirus_actualizaciones_so.md"
        }],
        "modo_vuln": 0,
        "aluc_det": 0,
        "proveedor": "groq",
        "tokens": 490,
        "justif": "Caso procesado exitosamente por el Respaldo Activo (Groq Llama 3.3) ante simulación de contingencia del proveedor primario."
    },

    # =========================================================================
    # 3. ESCALADOS A SOPORTE PRESENCIAL (escalado_cuadrilla) · 5 Tickets N3
    # =========================================================================
    {
        "codigo": "TCK-E01-BSOD",
        "estado": "escalado_cuadrilla",
        "cliente": "Roberto Silva (Finanzas - Puesto 08)",
        "email": "roberto.silva@empresa.com",
        "problema": "La computadora de escritorio emite tres pitidos cortos, huele a recalentamiento en la fuente de poder y se apaga arrojando pantalla azul BSOD KERNEL_DATA_INPAGE_ERROR.",
        "categoria": "Hardware y Equipos",
        "impacto": "Bajo",
        "urgencia": "Alta",
        "prioridad": "Alta",
        "sla": 15,
        "desc_sla": "Atención crítica e inmediata del técnico de TI en el puesto (menos de 15 min)",
        "solucion": "1. Apague el equipo y desconéctelo de la toma eléctrica por precaución.\n2. No intente encenderlo nuevamente.\n3. Se despachó un técnico de soporte presencial a su puesto con piezas de recambio.",
        "citas": [{
            "documento_id": "DOC-10_falla_estacion_trabajo_pc.md",
            "titulo_documento": "Diagnóstico Inicial ante Bloqueo, Pantalla Azul o Falla de Rendimiento en PC",
            "paso_exacto": "Paso 3: Diagnóstico Físico de Hardware, Memoria RAM y Fuente de Poder",
            "fragmento_aplicado": "«Falla física de energía: desconecte el equipo del tomacorriente por precaución. Un técnico de cuadrilla acudirá a su puesto con una fuente de poder y repuestos para revisarlo.»",
            "url": "https://soporte.pyme-estandar.org/manuales/DOC-10_falla_estacion_trabajo_pc.md"
        }],
        "modo_vuln": 0,
        "aluc_det": 0,
        "proveedor": "gemini",
        "tokens": 520,
        "justif": "Avería física no solucionable por software. Escalado Nivel 3 con confirmación de soporte presencial.",
        "cuadrilla_despachada": 1,
        "orden_despacho_id": "SITIO-TI-01",
        "confirmado_por": "Christian Morales (Tech Lead)"
    },
    {
        "codigo": "TCK-E02-CABLE",
        "estado": "escalado_cuadrilla",
        "cliente": "Lucía Mora (Sala de Juntas Principal)",
        "email": "lucia.mora@empresa.com",
        "problema": "La roseta de red de pared RJ-45 de la sala de reuniones se desprendió físicamente y el cable de red UTP tiene el conector quebrado impidiendo las videoconferencias de Directorio.",
        "categoria": "Red y Conectividad",
        "impacto": "Medio",
        "urgencia": "Alta",
        "prioridad": "Alta",
        "sla": 30,
        "desc_sla": "Atención departamental en menos de 30 minutos",
        "solucion": "1. No intente reparar el cable con cinta ni forzar el conector.\n2. Un técnico de cuadrilla acudirá con herramientas para instalar una toma nueva y un cable certificado.\n3. Se probará la videollamada antes de su reunión de Directorio.",
        "citas": [{
            "documento_id": "DOC-07_conectividad_red_cableada_oficina.md",
            "titulo_documento": "Diagnóstico y Solución de Conexión a Internet y Red Cableada en Oficina",
            "paso_exacto": "Paso 3: Crimpado de Conector RJ-45 y Reemplazo de Patchcord UTP Cat 6",
            "fragmento_aplicado": "«Daño físico en el cable de red de la sala: no jale el cable dañado. Un técnico presencial acudirá a reemplazar la roseta de pared y colocar un cable nuevo para las reuniones.»",
            "url": "https://soporte.pyme-estandar.org/manuales/DOC-07_conectividad_red_cableada_oficina.md"
        }],
        "modo_vuln": 0,
        "aluc_det": 0,
        "proveedor": "gemini",
        "tokens": 490,
        "justif": "Daño físico en infraestructura pasiva de red. Escalamiento presencial validado bajo compuerta HITL.",
        "cuadrilla_despachada": 1,
        "orden_despacho_id": "SITIO-TI-02",
        "confirmado_por": "Fernando Ribera (Builder)"
    },
    {
        "codigo": "TCK-E03-MONITOR",
        "estado": "escalado_cuadrilla",
        "cliente": "Estefanía Andrade (Diseño y Marketing)",
        "email": "estefania.andrade@empresa.com",
        "problema": "El segundo monitor de trabajo parpadea en negro constantemente; se probó con otro cable HDMI y el puerto DisplayPort de la tarjeta gráfica presenta falso contacto físico.",
        "categoria": "Hardware y Periféricos",
        "impacto": "Bajo",
        "urgencia": "Media",
        "prioridad": "Baja",
        "sla": 480,
        "desc_sla": "Atención en la jornada laboral (8 horas)",
        "solucion": "1. Verifique que los cables de corriente y de video del monitor estén firmes.\n2. Un técnico presencial acudirá a su puesto a probar con otro conector.\n3. Si la falla persiste, se le dejará un monitor de respaldo temporal para que continúe trabajando.",
        "citas": [{
            "documento_id": "DOC-14_perifericos_pantallas_oficina.md",
            "titulo_documento": "Instalación de Pantallas Dobles, Periféricos y Estaciones de Trabajo",
            "paso_exacto": "Paso 2: Verificación de Tarjeta de Video, Puerto DisplayPort y Reemplazo",
            "fragmento_aplicado": "«Falso contacto en la pantalla: asegúrese de que el cable de video no esté doblado. Un técnico presencial acudirá a revisar el puerto o entregarle un monitor de respaldo temporal.»",
            "url": "https://soporte.pyme-estandar.org/manuales/DOC-14_perifericos_pantallas_oficina.md"
        }],
        "modo_vuln": 0,
        "aluc_det": 0,
        "proveedor": "gemini",
        "tokens": 440,
        "justif": "Intervención física de hardware para diagnóstico de periférico y reposición desde bodega.",
        "cuadrilla_despachada": 1,
        "orden_despacho_id": "SITIO-TI-03",
        "confirmado_por": "Amalia Iguasnia (QA)"
    },
    {
        "codigo": "TCK-E04-SWITCH",
        "estado": "escalado_cuadrilla",
        "cliente": "Marcos Paredes (Departamento de Ventas)",
        "email": "marcos.paredes@empresa.com",
        "problema": "El switch de red local del área de ventas no enciende sus luces frontales tras el bajón de luz y las 6 estaciones de trabajo del sector se quedaron sin red ni telefonía IP.",
        "categoria": "Red y Conectividad",
        "impacto": "Alto",
        "urgencia": "Alta",
        "prioridad": "Alta",
        "sla": 15,
        "desc_sla": "Atención crítica e inmediata del técnico de TI (menos de 15 min)",
        "solucion": "1. Incidente colectivo reportado en el sector de ventas.\n2. El equipo de redes está revisando la caja de comunicaciones y el regulador de energía.\n3. Se restablecerá la conexión de las 6 computadoras y teléfonos en los próximos minutos.",
        "citas": [{
            "documento_id": "DOC-15_matriz_itil_gestion_incidentes.md",
            "titulo_documento": "Procedimiento Operativo Estándar ITIL 4 para Triaje, Priorización y Escalamiento",
            "paso_exacto": "Paso 3: Procedimiento de Escalamiento Inmediato a Soporte Presencial",
            "fragmento_aplicado": "«Interrupción general del sector: el conmutador principal de ventas se apagó tras la variación eléctrica. Se despachó soporte presencial de emergencia para restablecer la red del área.»",
            "url": "https://soporte.pyme-estandar.org/manuales/DOC-15_matriz_itil_gestion_incidentes.md"
        }],
        "modo_vuln": 0,
        "aluc_det": 0,
        "proveedor": "gemini",
        "tokens": 530,
        "justif": "Incidente crítico de infraestructura de área completa (Impacto Alto x Urgencia Alta = Prioridad Alta, SLA 15m).",
        "cuadrilla_despachada": 1,
        "orden_despacho_id": "SITIO-TI-04",
        "confirmado_por": "Christian Morales (Tech Lead)"
    },
    {
        "codigo": "TCK-E05-DISCO",
        "estado": "escalado_cuadrilla",
        "cliente": "Raúl Noboa (Archivo y Documentación)",
        "email": "raul.noboa@empresa.com",
        "problema": "El disco duro mecánico secundario de la estación emite ruidos metálicos repetitivos (clic rítmico) y el sistema operativo no monta la unidad de respaldo de proyectos.",
        "categoria": "Hardware y Equipos",
        "impacto": "Bajo",
        "urgencia": "Alta",
        "prioridad": "Alta",
        "sla": 15,
        "desc_sla": "Atención crítica e inmediata del técnico de TI en el puesto (menos de 15 min)",
        "solucion": "1. Apague la computadora de inmediato para no dañar el disco mecánico.\n2. No intente ejecutar programas de recuperación.\n3. Un técnico presencial acudirá a su puesto a extraer la unidad y clonar sus proyectos a un disco nuevo.",
        "citas": [{
            "documento_id": "DOC-13_respaldo_recuperacion_archivos.md",
            "titulo_documento": "Política y Procedimiento de Respaldo y Recuperación de Archivos de Trabajo",
            "paso_exacto": "Paso 3: Extracción Física Preventiva y Clonación de Unidad en Laboratorio",
            "fragmento_aplicado": "«Avería física en el disco: apague la computadora de inmediato para proteger sus archivos y no forzar el equipo. Un técnico presencial retirará la unidad para respaldar sus datos.»",
            "url": "https://soporte.pyme-estandar.org/manuales/DOC-13_respaldo_recuperacion_archivos.md"
        }],
        "modo_vuln": 0,
        "aluc_det": 0,
        "proveedor": "gemini",
        "tokens": 505,
        "justif": "Riesgo inminente de pérdida física de datos. Escalamiento presencial urgente aprobado en HITL.",
        "cuadrilla_despachada": 1,
        "orden_despacho_id": "SITIO-TI-05",
        "confirmado_por": "Fernando Ribera (Builder)"
    },

    # =========================================================================
    # 4. RESUELTOS (resuelto) · 5 Tickets: Validación y Cierre Satisfactorio
    # =========================================================================
    {
        "codigo": "TCK-R01-AD",
        "estado": "resuelto",
        "cliente": "Gonzalo Benítez (Logística)",
        "email": "gonzalo.benitez@empresa.com",
        "problema": "Olvido de contraseña de red tras el período de vacaciones. Se requería restablecimiento formal bajo política de seguridad.",
        "categoria": "Accesos y Contraseñas",
        "impacto": "Bajo",
        "urgencia": "Media",
        "prioridad": "Baja",
        "sla": 480,
        "desc_sla": "Atención en la jornada laboral (8 horas)",
        "solucion": "Contraseña temporal entregada al colaborador. Se confirmó que ingresó exitosamente y configuró su nueva clave personal.",
        "citas": [{
            "documento_id": "DOC-01_restablecimiento_contrasenas.md",
            "titulo_documento": "Procedimiento para Restablecimiento de Contraseñas de Dominio Windows y Correo Corporativo",
            "paso_exacto": "Paso 2: Generación de Contraseña Temporal Obligando Cambio",
            "fragmento_aplicado": "«Su clave fue restablecida: ingrese con la contraseña temporal entregada por el técnico. Al entrar, Windows le solicitará crear su nueva contraseña personal de 12 caracteres.»",
            "url": "https://soporte.pyme-estandar.org/manuales/DOC-01_restablecimiento_contrasenas.md"
        }],
        "modo_vuln": 0,
        "aluc_det": 0,
        "proveedor": "gemini",
        "tokens": 390,
        "justif": "Ticket resuelto en 14 minutos. Colaborador confirmó acceso pleno y cierre de caso.",
        "confirmado_por": "Christian Morales (Tech Lead)",
        "notificacion_enviada": 1
    },
    {
        "codigo": "TCK-R02-VPN",
        "estado": "resuelto",
        "cliente": "Lorena Castillo (Talento Humano)",
        "email": "lorena.castillo@empresa.com",
        "problema": "Error de certificado digital caducado al iniciar cliente VPN desde estación remota en teletrabajo.",
        "categoria": "Red y VPN",
        "impacto": "Bajo",
        "urgencia": "Media",
        "prioridad": "Baja",
        "sla": 480,
        "desc_sla": "Atención en la jornada laboral (8 horas)",
        "solucion": "Certificado digital actualizado en el equipo de la colaboradora. Conexión VPN probada y funcionando con normalidad.",
        "citas": [{
            "documento_id": "DOC-02_configuracion_vpn_corporativa.md",
            "titulo_documento": "Guía de Conexión y Configuración de VPN Corporativa para Teletrabajo",
            "paso_exacto": "Paso 1: Importación del Certificado Raíz de la Empresa",
            "fragmento_aplicado": "«Certificado de seguridad renovado con éxito: abra FortiClient VPN y presione 'Conectar'. Ya tiene acceso completo a las carpetas y sistemas de la empresa desde su hogar.»",
            "url": "https://soporte.pyme-estandar.org/manuales/DOC-02_configuracion_vpn_corporativa.md"
        }],
        "modo_vuln": 0,
        "aluc_det": 0,
        "proveedor": "gemini",
        "tokens": 420,
        "justif": "Resolución remota satisfactoria dentro del tiempo de SLA comprometido.",
        "confirmado_por": "Fernando Ribera (Builder)",
        "notificacion_enviada": 1
    },
    {
        "codigo": "TCK-R03-PRINT",
        "estado": "resuelto",
        "cliente": "Jorge Villacís (Auditoría Interna)",
        "email": "jorge.villacis@empresa.com",
        "problema": "Atasco de papel en la bandeja multipropósito 1 de la impresora departamental del tercer piso.",
        "categoria": "Impresoras y Periféricos",
        "impacto": "Bajo",
        "urgencia": "Baja",
        "prioridad": "Baja",
        "sla": 1440,
        "desc_sla": "Atención regular / Autoatención guiada en 24 horas",
        "solucion": "Hojas atascadas retiradas cuidadosamente. Se realizó una impresión de prueba y la máquina quedó completamente operativa.",
        "citas": [{
            "documento_id": "DOC-03_impresoras_red_departamentales.md",
            "titulo_documento": "Guía de Conexión y Solución de Problemas en Impresoras Multifunción de Red",
            "paso_exacto": "Paso 1: Retiro Cuidadoso de Hojas Atascadas en el Sentido de Alimentación",
            "fragmento_aplicado": "«Atasco de papel solucionado: se retiraron las hojas trabadas de la bandeja posterior y se limpiaron los rodillos. La impresora ya está lista y funcionando con normalidad.»",
            "url": "https://soporte.pyme-estandar.org/manuales/DOC-03_impresoras_red_departamentales.md"
        }],
        "modo_vuln": 0,
        "aluc_det": 0,
        "proveedor": "gemini",
        "tokens": 375,
        "justif": "Mantenimiento correctivo ejecutado con éxito. Equipo operando con normalidad.",
        "confirmado_por": "Amalia Iguasnia (QA)",
        "notificacion_enviada": 1
    },
    {
        "codigo": "TCK-R04-ACCESO",
        "estado": "resuelto",
        "cliente": "Mónica Terán (Nueva Colaboradora de Facturación)",
        "email": "monica.teran@empresa.com",
        "problema": "Solicitud de alta de usuario y asignación de permisos al módulo de ventas y cobranzas del ERP.",
        "categoria": "Accesos y Permisos",
        "impacto": "Bajo",
        "urgencia": "Baja",
        "prioridad": "Baja",
        "sla": 1440,
        "desc_sla": "Atención regular / Autoatención guiada en 24 horas",
        "solucion": "Cuenta de usuario creada con permisos autorizados por la jefatura. Colaboradora validó su ingreso al módulo de ventas.",
        "citas": [{
            "documento_id": "DOC-12_solicitud_nuevos_accesos.md",
            "titulo_documento": "Procedimiento para Solicitud de Nuevos Accesos y Alta de Colaboradores",
            "paso_exacto": "Paso 2: Creación de Cuenta con Permisos de Rol Mínimo Necesario (RBAC)",
            "fragmento_aplicado": "«Su usuario corporativo fue creado y los permisos al sistema contable ERP fueron habilitados. Ya puede iniciar sesión con las credenciales entregadas por su jefatura.»",
            "url": "https://soporte.pyme-estandar.org/manuales/DOC-12_solicitud_nuevos_accesos.md"
        }],
        "modo_vuln": 0,
        "aluc_det": 0,
        "proveedor": "gemini",
        "tokens": 410,
        "justif": "Proceso de alta completado según política ISO 27002. Usuario validado por jefatura.",
        "confirmado_por": "Christian Morales (Tech Lead)",
        "notificacion_enviada": 1
    },
    {
        "codigo": "TCK-R05-BACKUP",
        "estado": "resuelto",
        "cliente": "Víctor Ramos (Gerencia de Operaciones)",
        "email": "victor.ramos@empresa.com",
        "problema": "Recuperación de versión previa de la hoja de cálculo de presupuestos borrada accidentalmente de la carpeta compartida.",
        "categoria": "Políticas y Almacenamiento",
        "impacto": "Bajo",
        "urgencia": "Alta",
        "prioridad": "Media",
        "sla": 120,
        "desc_sla": "Atención técnica en menos de 2 horas",
        "solucion": "Archivo de presupuestos restaurado desde la copia de seguridad de las 08:00 AM en la carpeta compartida.",
        "citas": [{
            "documento_id": "DOC-13_respaldo_recuperacion_archivos.md",
            "titulo_documento": "Política y Procedimiento de Respaldo y Recuperación de Archivos de Trabajo",
            "paso_exacto": "Paso 2: Restauración de Archivo desde Instantáneas de Volumen (VSS)",
            "fragmento_aplicado": "«Hoja de cálculo recuperada exitosamente: el archivo de presupuestos fue restaurado desde la copia de respaldo en la carpeta compartida sin ninguna pérdida de información.»",
            "url": "https://soporte.pyme-estandar.org/manuales/DOC-13_respaldo_recuperacion_archivos.md"
        }],
        "modo_vuln": 0,
        "aluc_det": 0,
        "proveedor": "gemini",
        "tokens": 445,
        "justif": "Restauración completada en 8 minutos cumpliendo política de retención de respaldos.",
        "confirmado_por": "Fernando Ribera (Builder)",
        "notificacion_enviada": 1
    }
]

def configurar_20_tickets_pyme():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    ahora_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Vaciar la tabla tickets completamente para eliminar todos los ejemplos anteriores
    cursor.execute("DELETE FROM tickets")

    # 2. Insertar exactamente los 20 tickets nuevos (5 por cada estado)
    for t in TICKETS_PYME:
        cursor.execute("""
            INSERT INTO tickets (
                ticket_codigo, fecha_creacion, nombre_cliente, email_cliente,
                descripcion_problema, categoria, impacto, urgencia, prioridad,
                sla_minutos, descripcion_sla, solucion_propuesta, citas_json,
                estado, requiere_revision_humana, proveedor_ia, modelo_ia,
                conmutado, motivo_conmutacion, latencia_ms, justificacion, sintomas_json,
                tokens_prompt, tokens_completado, tokens_total, modo_vulnerable, alucinacion_detectada,
                eliminado, confirmado_por, fecha_confirmacion, accion_confirmada,
                notificacion_enviada, cuadrilla_despachada, orden_despacho_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?, ?, ?, ?)
        """, (
            t["codigo"],
            ahora_iso,
            t["cliente"],
            t["email"],
            t["problema"],
            t["categoria"],
            t["impacto"],
            t["urgencia"],
            t["prioridad"],
            t["sla"],
            t["desc_sla"],
            t["solucion"],
            json.dumps(t["citas"]),
            t["estado"],
            1 if t.get("modo_vuln") or t["prioridad"] == "Alta" else 0,
            t["proveedor"],
            "gemini-3.5-flash-lite" if "gemini" in t["proveedor"] else "llama-3.3-70b-versatile",
            1 if t["proveedor"] == "groq" else 0,
            "Simulación Failover Automático por Cuota 429" if t["proveedor"] == "groq" else None,
            380.0,
            t["justif"],
            json.dumps([t["categoria"], t["prioridad"]]),
            t["tokens"] - 90,
            90,
            t["tokens"],
            t["modo_vuln"],
            t["aluc_det"],
            t.get("confirmado_por"),
            ahora_iso if t.get("confirmado_por") else None,
            "autorizar_alta" if t.get("confirmado_por") else None,
            1 if t.get("notificacion_enviada") else 0,
            1 if t.get("cuadrilla_despachada") else 0,
            t.get("orden_despacho_id")
        ))

    conn.commit()
    cursor.execute("VACUUM")
    conn.commit()

    # 3. Validar conteo final en consola
    conteo = cursor.execute("""
        SELECT estado, COUNT(*) 
        FROM tickets 
        WHERE (eliminado IS NULL OR eliminado = 0) 
        GROUP BY estado
        ORDER BY CASE estado
            WHEN 'nuevo' THEN 1
            WHEN 'en_atencion' THEN 2
            WHEN 'escalado_cuadrilla' THEN 3
            WHEN 'resuelto' THEN 4
            ELSE 5
        END
    """).fetchall()
    
    print("\n" + "=" * 75)
    print(" CONFIGURACIÓN DE TABLERO KANBAN CON 5 EJEMPLOS REALES DE SOPORTE TIC PARA PYMES")
    print("=" * 75)
    total_general = 0
    for est, total in conteo:
        print(f" * Estado: {est.upper():<22} -> {total} tickets activos")
        total_general += total
    conn.close()
    print("=" * 75)
    print(f" TOTAL TICKETS EN TABLERO: {total_general} (Exactamente 5 por categoría/columna)\n")

if __name__ == "__main__":
    configurar_20_tickets_pyme()
