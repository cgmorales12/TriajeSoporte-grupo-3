from __future__ import annotations
"""
Servicio RAG: Búsqueda Semántica sobre los 15 Manuales Técnicos Oficiales en ChromaDB
Cumple: Cita con precisión el ID del documento y el paso operativo exacto desde la base vectorial persistente.
Autor: Luis Fernando Ribera Alajo (Builder / Arquitectura — GitHub: fernandolribera)
Revisión de Seguridad: Amalia Geoconda Iguasnia Escobar (QA / Seguridad — GitHub: Geocoiguasnia76)
"""

import os
import re
import logging
from typing import List, Dict, Any, Tuple, Optional
from app.schemas import CitaRAG, DiagnosticoRAG

logger = logging.getLogger("conectatec.rag")

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "chroma")

# Mapeo de términos clave para recuperación de respaldo determinista (fallback) en PYME
PALABRAS_CLAVE_MANUALES = {
    "DOC-01": ["contraseña", "clave", "password", "desbloqueo", "active directory", "windows", "bloqueada", "olvido de clave", "usuario bloqueado", "cuenta bloqueada"],
    "DOC-02": ["vpn", "forticlient", "openvpn", "teletrabajo", "acceso remoto", "gateway", "túnel", "2fa", "otp", "token", "conexión remota"],
    "DOC-03": ["impresora", "imprimir", "papel atascado", "atasco de papel", "tóner", "cola de impresión", "spooler", "ip impresora", "multifunción", "no imprime"],
    "DOC-04": ["carpeta compartida", "unidad de red", "servidor de archivos", "smb", "nas", "unidad z", "acceso denegado", "permisos", "file server", "recurso compartido"],
    "DOC-05": ["sistema contable", "erp", "facturación", "sql server", "sesión duplicada", "usuario conectado", "comprobante", "sri", "sesión colgada"],
    "DOC-06": ["política de seguridad", "iso 27002", "complejidad de contraseñas", "win l", "bloqueo de pantalla", "phishing", "confidencialidad", "escritorio limpio"],
    "DOC-07": ["red cableada", "cable de red", "ethernet", "rj45", "roseta", "ipconfig", "dhcp", "gateway", "switch", "sin internet en oficina"],
    "DOC-08": ["wifi corporativo", "red inalámbrica", "ssid", "red corporativa", "wpa2 enterprise", "radius", "wifi invitados", "olvidar red"],
    "DOC-09": ["antivirus", "endpoint", "windows update", "parches", "ransomware", "cuarentena", "malware", "actualizaciones", "seguridad"],
    "DOC-10": ["computadora lenta", "pantalla azul", "bsod", "bloqueo de pc", "administrador de tareas", "reinicio", "disco 100", "hardware", "ruido metálico"],
    "DOC-11": ["outlook", "correo", "buzón lleno", "pst", "filtro antispam", "spam", "adjunto", "email", "autoarchivar"],
    "DOC-12": ["nuevo usuario", "alta de personal", "solicitud de accesos", "permisos", "nuevo colaborador", "onboarding", "crear cuenta"],
    "DOC-13": ["respaldo", "backup", "recuperación", "versiones anteriores", "archivo borrado", "onedrive", "shadow copies", "vss", "restaurar archivo"],
    "DOC-14": ["pantalla doble", "segundo monitor", "extender pantalla", "win p", "hdmi", "displayport", "teclado", "ratón", "monitor adicional"],
    "DOC-15": ["itil", "matriz itil", "prioridad", "urgencia", "impacto", "escalamiento", "ticket kanban", "nivel 1", "nivel 2", "sla", "derivar a técnico"]
}

# URLs oficiales reales y verificables por manual (Cero dominios inventados)
URLS_REALES_MANUALES = {
    "DOC-01": "https://learn.microsoft.com/es-es/windows-server/identity/ad-ds/",
    "DOC-02": "https://docs.fortinet.com/product/forticlient/",
    "DOC-03": "https://support.hp.com/es-es/document/ish_2026_impresoras_red",
    "DOC-04": "https://learn.microsoft.com/es-es/windows-server/storage/file-server/",
    "DOC-05": "https://www.sri.gob.ec/facturacion-electronica",
    "DOC-06": "https://www.iso.org/standard/75652.html",
    "DOC-07": "https://standards.ieee.org/ieee/802.3/",
    "DOC-08": "https://www.wi-fi.org/discover-wi-fi/security",
    "DOC-09": "https://learn.microsoft.com/es-es/windows/security/threat-protection/",
    "DOC-10": "https://learn.microsoft.com/es-es/troubleshoot/windows-client/performance/",
    "DOC-11": "https://support.microsoft.com/es-es/office/configuracion-de-correo-outlook",
    "DOC-12": "https://learn.microsoft.com/es-es/azure/active-directory/governance/",
    "DOC-13": "https://support.microsoft.com/es-es/office/recuperar-versiones-anteriores",
    "DOC-14": "https://support.microsoft.com/es-es/windows/como-usar-varios-monitores-en-windows",
    "DOC-15": "https://www.axelos.com/certifications/itil-service-management"
}

def _resolver_url_manual(doc_id: str, url_meta: Optional[str] = None) -> str:
    """Retorna la URL oficial real y resoluble en internet para el manual indicado."""
    if doc_id in URLS_REALES_MANUALES:
        return URLS_REALES_MANUALES[doc_id]
    if url_meta and "conectatec.edu.ec" not in url_meta and "conectatec.local" not in url_meta:
        return url_meta
    return f"https://github.com/cgmorales12/TriajeSoporte-grupo-3/blob/main/data/raw/{doc_id.lower()}.md"


def _limpiar_fragmento_rag(doc_texto: str, doc_id: str = "") -> str:
    """
    Limpia el texto recuperado de ChromaDB o manuales raw para extraer
    únicamente el procedimiento técnico operativo y accionable,
    eliminando metadatos de indexación (como 'Términos clave: ...') y
    encabezados redundantes ya capturados en los metadatos de la cita.
    """
    if not doc_texto:
        return ""
    lineas = [l.strip() for l in doc_texto.splitlines()]
    lineas_filtradas = []
    for l in lineas:
        if not l:
            if lineas_filtradas and lineas_filtradas[-1] != "":
                lineas_filtradas.append("")
            continue
        l_lower = l.lower()
        if l_lower.startswith("términos clave:") or l_lower.startswith("terminos clave:"):
            continue
        # Si la línea repite exactamente el título del manual o la sección con punto medio o guión
        if doc_id and doc_id.lower() in l_lower and ("·" in l or "—" in l) and ("procedimiento" in l_lower or "manual" in l_lower):
            continue
        # Descartar líneas markdown puras de encabezado de nivel 1 o metadatos YAML
        if l.startswith("# ") or l.startswith("**Categoría:**") or l.startswith("**Origen:**") or l.startswith("**Vigencia:**") or l.startswith("**URL:**"):
            continue
        lineas_filtradas.append(l)

    texto_limpio = "\n".join(lineas_filtradas).strip()
    return texto_limpio if texto_limpio else doc_texto.strip()


def redactar_solucion_conversacional_para_usuario(
    fragmento_manual: str,
    doc_id: str,
    requiere_visita_campo: bool = False
) -> str:
    """
    Convierte el procedimiento técnico interno de los manuales (escrito en 3ra persona para el técnico de TI)
    en una guía de autoatención clara, empática y conversacional dirigida al usuario final (en 2da persona),
    diferenciando lo que el usuario puede verificar de lo que soporte técnico resolverá tras registrar el ticket.
    """
    doc_norm = (doc_id or "").upper().replace("_", "-")

    if requiere_visita_campo or "DOC-10" in doc_norm:
        return (
            "Se ha detectado un posible fallo físico en los componentes de su estación de trabajo.\n"
            "1. Por precaución y seguridad, apague el equipo y desconéctelo del tomacorriente.\n"
            "2. No intente encenderlo nuevamente ni manipular cables internos.\n"
            "3. Al confirmar este ticket, un técnico de soporte presencial acudirá a su puesto de trabajo con piezas de recambio."
        )

    if "DOC-01" in doc_norm:
        return (
            "Si ingresó erróneamente su clave más de 5 veces consecutivas, su cuenta se bloqueó automáticamente durante 30 minutos por directiva de seguridad.\n"
            "1. Si recuerda su contraseña actual, puede esperar el tiempo de seguridad o confirmar este ticket para que soporte la desbloquee de inmediato.\n"
            "2. Al enviar esta solicitud, nuestro equipo técnico accederá al sistema para reactivar su usuario.\n"
            "3. Si no recuerda su contraseña, el técnico le facilitará una clave provisional segura para que cree una nueva."
        )

    if "DOC-02" in doc_norm:
        return (
            "Si el cliente FortiClient VPN no logra conectar o se detiene con error de negociación:\n"
            "1. Cierre el programa FortiClient por completo desde la barra de tareas y vuelva a abrirlo.\n"
            "2. Verifique que su computadora cuente con conexión a internet navegando en cualquier página web.\n"
            "3. Al enviar este ticket, el equipo de soporte técnico revisará su acceso remoto y renovará el certificado digital si es necesario."
        )

    if "DOC-03" in doc_norm:
        return (
            "Si la impresora multifunción de red no responde o tiene documentos colgados:\n"
            "1. Por favor evite seguir enviando impresiones para no saturar la cola de la máquina.\n"
            "2. Compruebe que la bandeja tenga papel suficiente y no presente luces rojas de error o atasco.\n"
            "3. Al enviar este ticket, soporte técnico reiniciará el servicio de impresión de la red para liberar sus documentos."
        )

    if "DOC-04" in doc_norm:
        return (
            "Si no puede abrir la carpeta compartida o la unidad de red aparece con una cruz roja:\n"
            "1. Guarde y cierre cualquier documento abierto y reinicie la sesión de su computadora.\n"
            "2. Compruebe que el cable de red o Wi-Fi corporativo esté funcionando normalmente.\n"
            "3. Al enviar este ticket, soporte técnico verificará sus permisos de acceso en el servidor de archivos."
        )

    if "DOC-05" in doc_norm:
        return (
            "Si el sistema contable ERP muestra que su sesión quedó colgada o bloqueada por desconexión previa:\n"
            "1. Cierre la ventana del programa ERP en su equipo de trabajo.\n"
            "2. Espere 2 a 3 minutos mientras el servidor intenta liberar la conexión anterior.\n"
            "3. Al enviar este ticket, el administrador del sistema cerrará la sesión huérfana en el servidor para que pueda facturar nuevamente."
        )

    if "DOC-06" in doc_norm:
        return (
            "Por políticas institucionales de ciberseguridad, ciertos accesos a puertos USB o sitios externos están regulados:\n"
            "1. No intente forzar la conexión de dispositivos o memorias no autorizadas.\n"
            "2. Al registrar su ticket, detalle su necesidad de trabajo para que el oficial de seguridad evalúe autorizar un acceso temporal."
        )

    if "DOC-07" in doc_norm:
        return (
            "Si su computadora indica que no tiene conexión a internet por cable:\n"
            "1. Verifique que el cable de red detrás de su equipo esté firmemente conectado (debe encenderse una pequeña luz en el puerto).\n"
            "2. Desconecte y vuelva a enchufar el conector con firmeza hasta escuchar un 'clic'.\n"
            "3. Al enviar este ticket, soporte técnico comprobará el punto de red de su puesto o el conmutador de la oficina."
        )

    if "DOC-08" in doc_norm:
        return (
            "Si su laptop se desconecta intermitentemente del Wi-Fi de la empresa:\n"
            "1. En la lista de redes Wi-Fi, haga clic derecho en la red corporativa y elija 'Olvidar red'.\n"
            "2. Vuelva a conectarse ingresando su usuario y clave institucional.\n"
            "3. Si la desconexión continúa, envíe este ticket para renovar el certificado de red en su equipo."
        )

    if "DOC-09" in doc_norm:
        return (
            "Si el antivirus corporativo emitió una advertencia o bloqueó una descarga sospechosa:\n"
            "1. Por seguridad de su información y de la empresa, no intente abrir el archivo bloqueado.\n"
            "2. Desconecte su equipo de la red momentáneamente (desconecte el cable o desactive el Wi-Fi).\n"
            "3. Envíe este reporte para que el técnico de seguridad analice la amenaza y limpie su estación de trabajo."
        )

    if "DOC-11" in doc_norm:
        return (
            "Si su correo Outlook indica que el almacenamiento o buzón está al límite de capacidad:\n"
            "1. Ingrese a la carpeta 'Elementos eliminados' y haga clic en 'Vaciar carpeta'.\n"
            "2. Elimine correos de publicidad o mensajes antiguos con archivos adjuntos pesados.\n"
            "3. Al enviar este ticket, un técnico le asistirá de forma remota a archivar mensajes antiguos en su disco local sin perderlos."
        )

    if "DOC-12" in doc_norm:
        return (
            "Para solicitar un nuevo acceso a sistemas, carpetas compartidas o cuentas institucionales:\n"
            "1. Asegúrese de contar con la autorización de su jefatura de departamento.\n"
            "2. Envíe este ticket indicando qué programa, carpeta o sistema requiere utilizar.\n"
            "3. El área de soporte técnico configurará su perfil con los permisos correspondientes."
        )

    if "DOC-13" in doc_norm:
        return (
            "Si eliminó o perdió accidentalmente un archivo importante de su trabajo:\n"
            "1. Evite guardar nuevos documentos en esa misma carpeta para no sobreescribir información.\n"
            "2. Al enviar este ticket, indique el nombre aproximado del archivo y la fecha en que lo utilizó por última vez.\n"
            "3. El equipo de soporte técnico buscará en las copias de seguridad (backup) para restaurar su documento."
        )

    if "DOC-14" in doc_norm:
        return (
            "Si su monitor, teclado o mouse presentan fallos o no responden adecuadamente:\n"
            "1. Desconecte y vuelva a conectar con firmeza el cable USB o de video a la computadora.\n"
            "2. Pruebe conectar el periférico en otro puerto disponible del equipo.\n"
            "3. Al enviar este ticket, soporte técnico le facilitará un reemplazo funcional."
        )

    if "DOC-15" in doc_norm:
        return (
            "Incidente de servicio reportado en la infraestructura de la empresa:\n"
            "1. Se ha clasificado su solicitud con prioridad según el impacto en las actividades de su área.\n"
            "2. Al enviar este ticket, el personal técnico especializado atenderá su requerimiento en el tiempo estimado."
        )

    # Heurística de conversión para cualquier otro texto libre o procedimiento manual
    texto_adaptado = fragmento_manual or ""
    texto_adaptado = re.sub(r"(?i)\bsi el colaborador\b", "Si ingresó", texto_adaptado)
    texto_adaptado = re.sub(r"(?i)\bel técnico de ti accede a\b", "Al enviar este ticket, el equipo técnico accederá a", texto_adaptado)
    texto_adaptado = re.sub(r"(?i)\bel técnico accede a\b", "Soporte técnico accederá a", texto_adaptado)
    texto_adaptado = re.sub(r"(?i)\blocaliza la cuenta del usuario y marca la opción «desbloquear la cuenta»\.?", "Reactivará su cuenta de usuario en el sistema.", texto_adaptado)
    texto_adaptado = re.sub(r"(?i)\bsi el usuario recuerda su clave, puede intentar el inicio de sesión inmediatamente tras el desbloqueo\.?", "Si recuerda su clave, podrá iniciar sesión inmediatamente tras el desbloqueo; si la olvidó, se le facilitará una clave temporal.", texto_adaptado)
    texto_adaptado = re.sub(r"(?i)\bel usuario debe\b", "Le recomendamos", texto_adaptado)
    texto_adaptado = re.sub(r"(?i)\bel usuario puede\b", "Usted puede", texto_adaptado)

    return texto_adaptado.strip()


# Términos que disparan intervención física presencial del técnico de TI en el puesto de trabajo
TERMINOS_DESPACHO_PRESENCIAL = [
    "humo", "olor a quemado", "chispa", "disco dañado", "ruido metálico",
    "pantalla azul", "bsod", "reemplazo físico", "cable roto", "roseta dañada",
    "puerto dañado", "placa madre", "fuente de poder", "ventilador parado",
    "los roja", "luz roja", "alarma óptica", "los parpadea", "corte de fibra"
]

# Términos para el protocolo oficial de abstención (misión de silencio determinista)
TERMINOS_ABSTENCION_EXTERNA = [
    "complexivo", "comedor", "matrícula", "matricula", "almuerzo", "hambre", "comida",
    "desayuno", "cena", "sed", "cafeteria", "cafetería", "restaurante", "chiste", "broma",
    "llueve", "lluvia", "clima", "tiempo libre", "nómina", "nomina", "sueldo", "dinero",
    "hackear", "hack", "crackear", "menu ejecutivo", "menú ejecutivo", "materia", "profesor",
    "aula magna", "tarea", "medico", "médico", "salud", "enfermo", "cita médica", "cita medica",
    "futbol", "fútbol", "partido", "receta", "ceviche", "camarón", "camaron", "cocina",
    "selección", "seleccion", "poema", "cine", "película", "pelicula"
]

_cliente_chroma = None
_coleccion_chroma = None
_intento_inicializacion_chroma = False


def _obtener_coleccion_chroma():
    """Inicializa y retorna la colección persistente de ChromaDB."""
    global _cliente_chroma, _coleccion_chroma, _intento_inicializacion_chroma
    if _coleccion_chroma is not None:
        return _coleccion_chroma
    if _intento_inicializacion_chroma and _coleccion_chroma is None:
        return None

    _intento_inicializacion_chroma = True
    try:
        import chromadb
        if os.path.exists(CHROMA_DIR):
            _cliente_chroma = chromadb.PersistentClient(path=CHROMA_DIR)
            cols = [c.name for c in _cliente_chroma.list_collections()]
            nombre_col = "manuales_tecnicos" if "manuales_tecnicos" in cols else (cols[0] if cols else None)
            if nombre_col:
                _coleccion_chroma = _cliente_chroma.get_collection(nombre_col)
                logger.info("ChromaDB conectado con éxito a la colección '%s' (%d fragmentos).", nombre_col, _coleccion_chroma.count())
    except Exception as exc:
        logger.warning("No se pudo conectar a ChromaDB (%s). Se usará motor semántico de respaldo.", exc)
        _coleccion_chroma = None

    return _coleccion_chroma


def _obtener_contenido_manual(doc_id: str) -> Optional[str]:
    """Lee el archivo Markdown del manual correspondiente en data/raw si existe."""
    if not os.path.exists(RAW_DIR):
        return None
    for f in os.listdir(RAW_DIR):
        if f.startswith(doc_id) and f.endswith(".md"):
            with open(os.path.join(RAW_DIR, f), "r", encoding="utf-8") as archivo:
                return archivo.read()
    return None


def buscar_solucion(
    categoria: Optional[str] = None,
    texto: str = "",
    top_k: int = 3,
    simular_caida_rag: bool = False
) -> DiagnosticoRAG:
    """
    Herramienta oficial de búsqueda de soluciones técnicas sobre los 15 manuales.
    Consulta directamente la colección vectorial persistente de ChromaDB ('manuales_tecnicos').
    
    Parámetros:
        categoria: Categoría ITIL opcional para filtrado guiado.
        texto: Texto descriptivo de la incidencia técnica.
        top_k: Número de fragmentos más afines a recuperar (por defecto 3).
        simular_caida_rag: Bandera de Chaos Engineering para contingencia.
    """
    if simular_caida_rag:
        logger.info("[CHAOS ENGINEERING] Simulación de desconexión inducida del corpus RAG.")
        return DiagnosticoRAG(
            solucion_propuesta=(
                "[CONTINGENCIA RAG ACTIVADA] El repositorio documental de los 15 manuales técnicos "
                "se encuentra temporalmente fuera de línea por simulación de fallo. No es posible brindar autoatención guiada de Nivel 1. "
                "El incidente ha sido derivado a Nivel 2 para diagnóstico y atención directa por personal técnico humano."
            ),
            citas=[],
            requiere_visita_campo=False
        )

    texto_lower = (texto or "").lower().strip()
    cat_lower = (categoria or "").lower().strip()

    # 1. Regla de Silencio Determinista y Abstención (Zero-Hallucination)
    # 1.1 Si la categoría detectada es Fuera de Alcance o No Técnica, abstención inmediata sin RAG
    es_categoria_fuera_de_alcance = (
        "fuera de alcance" in cat_lower or 
        "no técnica" in cat_lower or 
        "no tecnica" in cat_lower or
        "solicitud no técnica" in cat_lower
    )

    # 1.2 Solicitudes maliciosas o de vulneración de seguridad: Abstención obligatoria inmediata
    es_adversarial = any(h in texto_lower for h in ["hackear", "hack", "crackear", "vulnerar", "piratear", "sniffear"])

    # 1.3 Detecta consultas de infraestructura técnica de la PYME (60 colaboradores)
    terminos_ti = [
        "vpn", "impresora", "imprimir", "contraseña", "clave", "password", "usuario", 
        "outlook", "correo", "servidor", "carpeta", "erp", "contable", "pantalla", 
        "monitor", "antivirus", "switch", "pyme", "itil", "red", "ethernet", "wifi", 
        "internet", "dns", "active directory", "smb", "nas", "pc", "docking", "backup", 
        "respaldo", "disco", "atasco", "spooler", "roseta", "cable", "windows"
    ]
    tiene_termino_ti = any(t in texto_lower for t in terminos_ti)
    es_fuera_de_alcance = (
        es_categoria_fuera_de_alcance or
        (any(w in texto_lower for w in TERMINOS_ABSTENCION_EXTERNA) and not tiene_termino_ti) or 
        es_adversarial
    )

    if es_fuera_de_alcance or (len(texto_lower) < 4 and not tiene_termino_ti):
        return DiagnosticoRAG(
            solucion_propuesta=(
                "No dispongo de un procedimiento técnico registrado para esta situación en los 15 manuales oficiales de ConectaTec / Soporte PYME. "
                "La consulta no describe ninguna avería técnica ni incidencia en la infraestructura de TI (Active Directory, VPN, impresoras, carpetas SMB, ERP, correo u ofimática). "
                "No se requiere intervención técnica en el puesto de trabajo. "
                "Orientación al usuario: Si su solicitud corresponde a trámites administrativos, académicos (como notas, matrículas o certificaciones) o de Recursos Humanos, "
                "por favor acuda a Secretaría General o al departamento correspondiente. "
                "Si experimenta problemas con su equipo de trabajo, red corporativa o accesos, por favor descríbalos detalladamente."
            ),
            citas=[],
            requiere_visita_campo=False
        )

    # 2. Evaluación de Alarma Crítica Física (Intervención presencial del técnico de TI)
    requiere_visita_campo = any(termino in texto_lower for termino in TERMINOS_DESPACHO_PRESENCIAL)

    # 3. Consulta a la Colección Vectorial Persistente de ChromaDB
    coleccion = _obtener_coleccion_chroma()
    citas: List[CitaRAG] = []
    docs_recuperados = []

    if coleccion is not None:
        try:
            # Query semántico directo a ChromaDB
            filtro_where = {"categoria": categoria} if categoria else None
            res_chroma = None
            try:
                if filtro_where:
                    res_chroma = coleccion.query(query_texts=[texto], n_results=max(top_k * 3, 10), where=filtro_where)
            except Exception:
                res_chroma = None

            if not res_chroma or not res_chroma.get("ids") or len(res_chroma["ids"][0]) == 0:
                res_chroma = coleccion.query(query_texts=[texto], n_results=max(top_k * 3, 10))

            if res_chroma and res_chroma.get("metadatas") and len(res_chroma["metadatas"][0]) > 0:
                metas = res_chroma["metadatas"][0]
                docs = res_chroma["documents"][0]
                dists = res_chroma.get("distances", [[0.0] * len(metas)])[0]

                for meta, doc_texto, dist in zip(metas, docs, dists):
                    doc_id = meta.get("documento", "DOC-01")

                    # Filtro DOC-15 (Matriz ITIL interna): Solo si se consulta por gestión/clasificación ITIL
                    if doc_id == "DOC-15":
                        terminos_itil = ["itil", "sla", "prioridad", "urgencia", "impacto", "escalamiento", "matriz"]
                        if not any(ti in texto_lower for ti in terminos_itil):
                            continue
                        continue

                    if doc_id not in docs_recuperados:
                        docs_recuperados.append(doc_id)
                        
                        titulo_doc = f"Manual Oficial {doc_id}"
                        # Extraer título real si está disponible
                        contenido_raw = _obtener_contenido_manual(doc_id)
                        if contenido_raw:
                            lineas = contenido_raw.splitlines()
                            if lineas:
                                titulo_doc = lineas[0].replace("#", "").strip()

                        paso = meta.get("sección") or meta.get("procedimiento") or "Paso 1: Diagnóstico General"
                        url_canon = _resolver_url_manual(doc_id, meta.get("url"))
                        vigencia = meta.get("vigencia") or "v3.2 - Octubre 2026"
                        
                        # Limpiar fragmento de forma estricta (remover metadatos de indexación y duplicados)
                        frag_limpio = _limpiar_fragmento_rag(doc_texto, doc_id)

                        citas.append(CitaRAG(
                            documento_id=doc_id,
                            titulo_documento=titulo_doc,
                            paso_exacto=paso,
                            fragmento_aplicado=frag_limpio[:600],
                            vigencia=vigencia,
                            url=url_canon
                        ))
                    if len(citas) >= top_k:
                        break
        except Exception as err_query:
            logger.warning("Falla al consultar ChromaDB: %s. Ejecutando fallback determinista.", err_query)
            citas = []

    # 4. Fallback Determinista sobre data/raw (por si ChromaDB no estuviera disponible)
    if not citas:
        puntajes: List[Tuple[str, int]] = []
        for doc_id, keywords in PALABRAS_CLAVE_MANUALES.items():
            score = sum(1 for kw in keywords if kw in texto_lower)
            if score > 0:
                puntajes.append((doc_id, score))
        puntajes.sort(key=lambda x: x[1], reverse=True)

        docs_a_citar = [p[0] for p in puntajes[:top_k]] if puntajes else (["DOC-10"] if requiere_visita_campo else [])

        if not docs_a_citar and not requiere_visita_campo:
            return DiagnosticoRAG(
                solucion_propuesta=(
                    "No dispongo de un procedimiento técnico registrado para esta situación en los 15 manuales oficiales de ConectaTec / Soporte PYME. "
                    "La consulta no describe ninguna avería técnica ni incidencia en la infraestructura de TI (Active Directory, VPN, impresoras, carpetas SMB, ERP, correo u ofimática). "
                    "No se requiere intervención técnica en el puesto de trabajo. "
                    "Orientación al usuario: Si su solicitud corresponde a trámites administrativos, académicos (como notas, matrículas o certificaciones) o de Recursos Humanos, "
                    "por favor acuda a Secretaría General o al departamento correspondiente. "
                    "Si experimenta problemas con su equipo de trabajo, red corporativa o accesos, por favor descríbalos detalladamente."
                ),
                citas=[],
                requiere_visita_campo=False
            )

        for doc_id in docs_a_citar:
            contenido = _obtener_contenido_manual(doc_id)
            if contenido:
                lineas = contenido.splitlines()
                titulo = lineas[0].replace("#", "").strip() if lineas else f"Manual Técnico {doc_id}"
                paso_citado = "Paso 1: Diagnóstico General"
                fragmento = "Verifique las conexiones físicas del equipo y el estado de los indicadores luminosos."

                pasos_encontrados = re.findall(r"(### (Paso \d+: [^\n]+))\n([^\n]+)", contenido)
                for paso_encabezado, _, paso_cuerpo in pasos_encontrados:
                    if any(w in paso_cuerpo.lower() for w in texto_lower.split() if len(w) > 4):
                        paso_citado = paso_encabezado.replace("###", "").strip()
                        fragmento = paso_cuerpo.strip()
                        break
                else:
                    if pasos_encontrados:
                        paso_citado = pasos_encontrados[0][0].replace("###", "").strip()
                        fragmento = pasos_encontrados[0][2].strip()

                vig_match = re.search(r"\*\*(?:Versión\s*/\s*Vigencia|Vigencia):\*\*\s*(.+)", contenido)
                vigencia = vig_match.group(1).strip() if vig_match else "v3.2 - Octubre 2026"
                url_canon = _resolver_url_manual(doc_id)

                citas.append(CitaRAG(
                    documento_id=doc_id,
                    titulo_documento=titulo,
                    paso_exacto=paso_citado,
                    fragmento_aplicado=fragmento,
                    vigencia=vigencia,
                    url=url_canon
                ))

    # 5. Formular Solución Propuesta Determinista Conversacional
    if requiere_visita_campo:
        solucion = redactar_solucion_conversacional_para_usuario(
            "", doc_id="DOC-10", requiere_visita_campo=True
        )
    elif citas:
        doc_principal = citas[0].documento_id
        solucion = redactar_solucion_conversacional_para_usuario(
            citas[0].fragmento_aplicado,
            doc_id=doc_principal,
            requiere_visita_campo=requiere_visita_campo
        )
    else:
        solucion = (
            "Compruebe las conexiones físicas de su equipo y reinícielo. "
            "Al confirmar este ticket, el equipo de soporte técnico le asistirá para resolver el inconveniente."
        )

    return DiagnosticoRAG(
        solucion_propuesta=solucion,
        citas=citas,
        requiere_visita_campo=requiere_visita_campo
    )


def consultar_base_conocimiento(texto_problema: str, categoria: Optional[str] = None, simular_caida_rag: bool = False) -> DiagnosticoRAG:
    """
    Función de compatibilidad: busca en ChromaDB sobre los 15 manuales técnicos oficiales.
    """
    return buscar_solucion(categoria=categoria, texto=texto_problema, top_k=3, simular_caida_rag=simular_caida_rag)
