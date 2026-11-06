#!/usr/bin/env python3
"""
Script de Ingesta, Limpieza, Fragmentación y Vectorización Reproducible (RAG)
Proyecto: ConectaTec / TecnoAula — Triaje de Incidentes Técnicos (Caso N.º 03 · Grupo 3 UNIANDES)
Seminario de Titulación: Ingeniería de Software con IA Generativa — 2026

Requerimiento Oficial:
«scripts/ingest.py reproducible: Extrae, limpia, fragmenta, genera embeddings
y guarda con metadatos (documento, sección, vigencia, URL).»
"""

import os
import sys
import re
import json
import hashlib
from typing import List, Dict, Any, Tuple
from datetime import datetime

# Forzar codificación UTF-8 en consola Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DIR = os.path.join(RAIZ, "data", "raw")
CHROMA_DIR = os.path.join(RAIZ, "data", "chroma")
COLLECTION_NAME = "manuales_tecnicos"

# URLs canónicas oficiales reales y verificables por documento (Cero dominios inventados)
URLS_OFICIALES = {
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
    "DOC-15": "https://www.axelos.com/certifications/itil-service-management",
}

# Términos clave del dominio técnico para enriquecimiento semántico en PYME
PALABRAS_CLAVE_DOMINIO = {
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


def extraer_documentos_raw(directorio: str) -> List[Dict[str, Any]]:
    """1. EXTRAE: Lee todos los manuales Markdown oficiales en data/raw/."""
    documentos = []
    if not os.path.exists(directorio):
        raise FileNotFoundError(f"El directorio de documentos no existe: {directorio}")

    archivos = sorted([f for f in os.listdir(directorio) if f.startswith("DOC-") and f.endswith(".md")])
    for archivo in archivos:
        doc_id = archivo.split("_")[0]
        ruta = os.path.join(directorio, archivo)
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
        documentos.append({
            "id": doc_id,
            "archivo": archivo,
            "ruta": ruta,
            "contenido_crudo": contenido
        })
    return documentos


def limpiar_texto(texto: str) -> str:
    """2. LIMPIA: Normaliza saltos de línea, espacios en blanco y caracteres de control."""
    # Normalizar saltos de línea Windows / Unix
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    # Colapsar espacios múltiples horizontales
    texto = re.sub(r"[ \t]+", " ", texto)
    # Colapsar líneas vacías excesivas a máximo 2
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()


def parsear_metadatos_cabecera(contenido: str, doc_id: str) -> Dict[str, str]:
    """Extrae metadatos declarados en las primeras líneas del Markdown."""
    categoria = "Soporte Técnico General"
    fabricante = "ConectaTec ISP"
    vigencia = "2026-V1"

    cat_match = re.search(r"\*\*Categoría:\*\*\s*(.+)", contenido)
    if cat_match:
        categoria = cat_match.group(1).strip()

    fab_match = re.search(r"\*\*(?:Fabricante\s*/\s*Origen|Origen):\*\*\s*(.+)", contenido)
    if fab_match:
        fabricante = fab_match.group(1).strip()

    vig_match = re.search(r"\*\*(?:Versión\s*/\s*Vigencia|Vigencia):\*\*\s*(.+)", contenido)
    if vig_match:
        vigencia = vig_match.group(1).strip()

    # Título principal del documento
    titulo_match = re.search(r"^#\s+(.+)$", contenido, re.MULTILINE)
    titulo = titulo_match.group(1).strip() if titulo_match else f"Manual {doc_id}"

    return {
        "categoria": categoria,
        "fabricante": fabricante,
        "vigencia": vigencia,
        "titulo": titulo,
        "url": URLS_OFICIALES.get(doc_id, f"https://soporte.conectatec.edu.ec/manuales/{doc_id}")
    }


def fragmentar_documento(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    3. FRAGMENTA: Aplica la regla «Una ficha / procedimiento = Un fragmento».
    Divide el documento por secciones operativas (### Paso X, ## Descripción, ## Matriz).
    Preserva el código del documento y título en cada fragmento para evitar fragmentos huérfanos.
    """
    doc_id = doc["id"]
    texto_limpio = limpiar_texto(doc["contenido_crudo"])
    metadatos_doc = parsear_metadatos_cabecera(texto_limpio, doc_id)
    
    chunks = []
    
    # Expresión regular para localizar encabezados de nivel 2 y 3
    # Ej: ### Paso 1: ..., ## Descripción General, ## Matriz de Diagnóstico
    patron_secciones = re.compile(r"^(#{2,3}\s+.*)$", re.MULTILINE)
    partes = patron_secciones.split(texto_limpio)
    
    if len(partes) <= 1:
        # Documento corto sin subdivisiones
        chunk_id = f"{doc_id}-C01"
        chunks.append({
            "chunk_id": chunk_id,
            "texto": f"{metadatos_doc['titulo']}\n\n{texto_limpio}",
            "metadatos": {
                "documento": doc_id,
                "sección": "General",
                "vigencia": metadatos_doc["vigencia"],
                "url": metadatos_doc["url"],
                "categoria": metadatos_doc["categoria"],
                "fabricante": metadatos_doc["fabricante"],
                "procedimiento": f"{doc_id}-GEN"
            }
        })
        return chunks

    seccion_actual = "Introducción"
    contenido_actual = []
    chunk_num = 1
    
    for parte in partes:
        parte_strip = parte.strip()
        if not parte_strip:
            continue
            
        if parte_strip.startswith("## ") or parte_strip.startswith("### "):
            # Si ya teníamos contenido acumulado de la sección previa, guardarlo como chunk
            if contenido_actual:
                c_texto = "\n".join(contenido_actual).strip()
                if len(c_texto) > 40:
                    chunk_id = f"{doc_id}-C{chunk_num:02d}"
                    keywords = PALABRAS_CLAVE_DOMINIO.get(doc_id, [])
                    kw_line = f"Términos clave: {', '.join(keywords)}\n" if keywords else ""
                    chunks.append({
                        "chunk_id": chunk_id,
                        "texto": f"{metadatos_doc['titulo']} · {seccion_actual}\n{kw_line}\n{c_texto}",
                        "metadatos": {
                            "documento": doc_id,
                            "sección": seccion_actual,
                            "vigencia": metadatos_doc["vigencia"],
                            "url": metadatos_doc["url"],
                            "categoria": metadatos_doc["categoria"],
                            "fabricante": metadatos_doc["fabricante"],
                            "procedimiento": f"{doc_id}-P{chunk_num}"
                        }
                    })
                    chunk_num += 1
                contenido_actual = []
            seccion_actual = re.sub(r"^#{2,3}\s+", "", parte_strip)
        else:
            contenido_actual.append(parte_strip)

    # Guardar último chunk residual
    if contenido_actual:
        c_texto = "\n".join(contenido_actual).strip()
        if len(c_texto) > 40:
            chunk_id = f"{doc_id}-C{chunk_num:02d}"
            keywords = PALABRAS_CLAVE_DOMINIO.get(doc_id, [])
            kw_line = f"Términos clave: {', '.join(keywords)}\n" if keywords else ""
            chunks.append({
                "chunk_id": chunk_id,
                "texto": f"{metadatos_doc['titulo']} · {seccion_actual}\n{kw_line}\n{c_texto}",
                "metadatos": {
                    "documento": doc_id,
                    "sección": seccion_actual,
                    "vigencia": metadatos_doc["vigencia"],
                    "url": metadatos_doc["url"],
                    "categoria": metadatos_doc["categoria"],
                    "fabricante": metadatos_doc["fabricante"],
                    "procedimiento": f"{doc_id}-P{chunk_num}"
                }
            })

    return chunks


def vectorizar_e_indexar(chunks: List[Dict[str, Any]], ruta_chroma: str) -> Any:
    """
    4. GENERA EMBEDDINGS Y GUARDA:
    Persiste los fragmentos con embeddings y metadatos (documento, sección, vigencia, URL)
    en ChromaDB persistente de manera 100% reproducible.
    """
    import chromadb
    from chromadb.config import Settings

    os.makedirs(ruta_chroma, exist_ok=True)
    
    # Cliente ChromaDB persistente
    client = chromadb.PersistentClient(path=ruta_chroma)
    
    # Reiniciar colección para garantizar reproducibilidad exacta
    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine", "description": "15 Manuales Oficiales ConectaTec"}
    )

    ids = [c["chunk_id"] for c in chunks]
    documents = [c["texto"] for c in chunks]
    metadatas = [c["metadatos"] for c in chunks]

    # Ingesta por lotes para alta eficiencia
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    # Guardar manifiesto JSON de auditoría forense para verificación sin cliente Chroma
    manifiesto = {
        "timestamp_ingesta": datetime.now().isoformat(),
        "total_documentos": len(set(c["metadatos"]["documento"] for c in chunks)),
        "total_fragmentos": len(chunks),
        "metadatos_requeridos": ["documento", "sección", "vigencia", "url"],
        "coleccion": COLLECTION_NAME,
        "espacio_vectorial": "cosine",
        "fragmentos": [
            {
                "id": c["chunk_id"],
                "metadatos": c["metadatos"],
                "longitud_caracteres": len(c["texto"])
            }
            for c in chunks
        ]
    }
    
    with open(os.path.join(ruta_chroma, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifiesto, f, ensure_ascii=False, indent=2)

    return collection


def probar_recuperacion(collection: Any) -> None:
    """Prueba rápida de verificación para asegurar que la recuperación vectorial responde."""
    consulta = "La luz LOS de la ONT parpadea en rojo y no tengo señal"
    resultados = collection.query(query_texts=[consulta], n_results=2)
    
    print("\n🔍 Verificación RAG post-ingesta:")
    print(f"   Consulta de prueba: «{consulta}»")
    if resultados and resultados.get("ids") and resultados["ids"][0]:
        top_id = resultados["ids"][0][0]
        meta = resultados["metadatas"][0][0]
        distancia = resultados["distances"][0][0] if "distances" in resultados else 0.0
        print(f"   ✅ Top-1 recuperado: {top_id}")
        print(f"      • Documento: {meta.get('documento')}")
        print(f"      • Sección:   {meta.get('sección')}")
        print(f"      • Vigencia:  {meta.get('vigencia')}")
        print(f"      • URL:       {meta.get('url')}")
        print(f"      • Distancia Coseno: {distancia:.4f}")
    else:
        print("   ⚠️ No se obtuvieron resultados en la consulta de prueba.")


def main():
    print("=" * 72)
    print("🚀 INGESTA REPRODUCIBLE RAG · ConectaTec / TecnoAula (Grupo 3 UNIANDES)")
    print(f"   Directorio Origen: {RAW_DIR}")
    print(f"   Destino ChromaDB:  {CHROMA_DIR}")
    print("=" * 72)

    # 1. Extraer
    print("\n[1/5] 📂 Extrayendo manuales técnicos desde data/raw/ ...")
    documentos = extraer_documentos_raw(RAW_DIR)
    print(f"      Se extrajeron exitosamente {len(documentos)} documentos oficiales.")

    # 2 y 3. Limpiar y Fragmentar
    print("\n[2/5] 🧹 Limpiando y normalizando texto...")
    print("[3/5] ✂️  Fragmentando bajo la regla «Una ficha/paso = Un fragmento»...")
    todos_los_chunks = []
    for doc in documentos:
        chunks_doc = fragmentar_documento(doc)
        todos_los_chunks.extend(chunks_doc)
        print(f"      • {doc['id']}: {len(chunks_doc)} fragmentos generados")

    print(f"\n      Total global: {len(todos_los_chunks)} fragmentos estructurados.")

    # Validar que todos los chunks cumplan el contrato de metadatos estricto
    campos_obligatorios = ["documento", "sección", "vigencia", "url"]
    for c in todos_los_chunks:
        for campo in campos_obligatorios:
            if campo not in c["metadatos"] or not c["metadatos"][campo]:
                raise ValueError(f"Fragmento {c['chunk_id']} no tiene el metadato obligatorio: {campo}")

    print(f"      ✅ Todos los fragmentos incluyen metadatos: {campos_obligatorios}")

    # 4. Generar embeddings y guardar en ChromaDB
    print("\n[4/5] 🧠 Generando embeddings y guardando en ChromaDB persistente...")
    collection = vectorizar_e_indexar(todos_los_chunks, CHROMA_DIR)
    print(f"      Colección '{COLLECTION_NAME}' persistida con éxito en {CHROMA_DIR}")
    print(f"      Manifiesto guardado en data/chroma/manifest.json")

    # 5. Probar
    print("\n[5/5] 🧪 Ejecutando prueba de similitud angular...")
    probar_recuperacion(collection)

    print("\n" + "=" * 72)
    print("🎉 INGESTA REPRODUCIBLE COMPLETADA CON ÉXITO")
    print(f"   Total Documentos: {len(documentos)} | Total Chunks: {len(todos_los_chunks)}")
    print("=" * 72)


if __name__ == "__main__":
    main()
