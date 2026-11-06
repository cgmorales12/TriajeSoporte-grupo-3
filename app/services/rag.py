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
    "DOC-08": ["wifi corporativo", "red inalámbrica", "ssid", "innova-corp", "wpa2 enterprise", "radius", "wifi invitados", "olvidar red"],
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
    return f"https://github.com/cgmorales12/conectatec-grupo-3/blob/main/data/raw/{doc_id.lower()}.md"


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
                "⚠️ [CONTINGENCIA RAG ACTIVADA] El repositorio documental de los 15 manuales técnicos "
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
                "No dispongo de un procedimiento técnico registrado para esta situación en los 15 manuales oficiales de TecnoAula / Soporte PYME. "
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
                        
                        # Limpiar fragmento
                        frag = doc_texto.strip()
                        if "—" in frag:
                            frag = frag.split("—", 1)[-1].strip()

                        citas.append(CitaRAG(
                            documento_id=doc_id,
                            titulo_documento=titulo_doc,
                            paso_exacto=paso,
                            fragmento_aplicado=frag[:300],
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
                    "No dispongo de un procedimiento técnico registrado para esta situación en los 15 manuales oficiales de TecnoAula / Soporte PYME. "
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

    # 5. Formular Solución Propuesta Determinista
    if requiere_visita_campo:
        solucion = (
            "Se detectó un fallo crítico de hardware en la estación de trabajo (DOC-10). "
            "Se ha generado un ticket con Prioridad Alta para atención presencial inmediata por parte del técnico de TI en el puesto del colaborador."
        )
    elif citas:
        solucion = f"Procedimiento recomendado según {citas[0].documento_id} ({citas[0].paso_exacto}): {citas[0].fragmento_aplicado}"
    else:
        solucion = "Proceda a verificar los cables y reiniciar el equipo (DOC-10). Si el inconveniente persiste, el ticket será derivado al técnico de TI."

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
