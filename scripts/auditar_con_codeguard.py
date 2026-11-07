# -*- coding: utf-8 -*-
"""
Auditor de Seguridad de Código con CodeGuard (Grupo 10 · UNIANDES)
Analiza los componentes clave de app/ contra la API en Railway de CodeGuard.
"""

import os
import sys
import json
import urllib.request
import urllib.error

API_BASE = "https://revisor-inteligente-codigo-production.up.railway.app"
ENDPOINT_ESTATICO = f"{API_BASE}/api/v1/estatico/analizar"
ENDPOINT_ANALIZAR = f"{API_BASE}/api/v1/analizar"

ARCHIVOS_AUDITAR = [
    ("app/tools/priorizar.py", "Lógica determinista ITIL de cálculo de prioridad"),
    ("app/routers/salud.py", "Endpoint de salud desacoplado /health"),
    ("app/routers/auth.py", "Gestión de sesiones y credenciales de técnicos"),
    ("app/services/conversor.py", "Saneamiento de texto y mitigación de XSS"),
    ("app/flujo.py", "Máquina de estados determinista de tickets"),
    ("app/routers/manuales.py", "Descarga y consulta de manuales oficiales"),
    ("app/database.py", "Persistencia SQLite con consultas parametrizadas (?)"),
    ("app/main.py", "Perímetro FastAPI, CORS, middlewares y Token Bucket"),
    ("app/schemas.py", "Contratos Pydantic V2 con extra='forbid'"),
    ("app/services/llm.py", "Integración LLM con anonimización y fallback"),
]

def enviar_analisis(endpoint, archivo_nom, codigo_texto):
    """Envía un fragmento de código a CodeGuard"""
    # Truncar limpiamente respetando declaraciones de funciones completas
    if len(codigo_texto) > 11500:
        corte_def = codigo_texto[:11500].rfind("\ndef ")
        if corte_def > 2000:
            codigo_texto = codigo_texto[:corte_def]
        else:
            corte_nl = codigo_texto[:11500].rfind("\n")
            codigo_texto = codigo_texto[:corte_nl]
    
    payload = json.dumps({
        "archivo": archivo_nom,
        "codigo": codigo_texto
    }).encode("utf-8")
    
    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            data = resp.read().decode("utf-8")
            return json.loads(data), None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        return None, f"HTTP {e.code}: {error_body[:200]}"
    except Exception as e:
        return None, str(e)


def main():
    print("=" * 80)
    print("🛡️  AUDITORÍA DE SEGURIDAD CON CODEGUARD (REVISOR INTELIGENTE)")
    print(f"    API Remota: {API_BASE}")
    print("    Proyecto Auditado: Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME · Grupo 3 UNIANDES")
    print("=" * 80)
    
    resultados_estaticos = []
    
    for ruta_rel, descripcion in ARCHIVOS_AUDITAR:
        if not os.path.exists(ruta_rel):
            print(f"⚠️ Archivo no encontrado: {ruta_rel}")
            continue
            
        with open(ruta_rel, "r", encoding="utf-8", errors="replace") as f:
            contenido = f.read()
            
        print(f"\n🔍 Auditando: {ruta_rel} ({len(contenido)} caracteres)")
        print(f"   Propósito: {descripcion}")
        
        # 1. Análisis Estático (Bandit + Ruff)
        res_est, err_est = enviar_analisis(ENDPOINT_ESTATICO, os.path.basename(ruta_rel), contenido)
        if res_est:
            estado = res_est.get("estado", "desconocido")
            hallazgos = res_est.get("hallazgos", [])
            herramientas = res_est.get("herramientas", [])
            
            print(f"   • Análisis Estático: {estado.upper()}")
            for h in herramientas:
                print(f"     - {h.get('herramienta')}: estado {h.get('estado')} | hallazgos: {h.get('hallazgos')}")
                
            if hallazgos:
                print(f"     ⚠️ Hallazgos detectados ({len(hallazgos)}):")
                for h in hallazgos:
                    print(f"       [{h.get('nivel')}] {h.get('regla')}: {h.get('mensaje')} (Línea {h.get('linea')})")
            else:
                print("     ✅ CERO HALLAZGOS DE VULNERABILIDAD.")
                
            resultados_estaticos.append({
                "archivo": ruta_rel,
                "descripcion": descripcion,
                "hallazgos": len(hallazgos),
                "detalle_hallazgos": hallazgos,
                "herramientas": herramientas
            })
        else:
            print(f"   ❌ Error en análisis estático: {err_est}")

    print("\n" + "=" * 80)
    print("📊 RESUMEN FINAL DE LA AUDITORÍA DE SEGURIDAD")
    print("=" * 80)
    total_archivos = len(resultados_estaticos)
    total_limpios = sum(1 for r in resultados_estaticos if r["hallazgos"] == 0)
    total_hallazgos = sum(r["hallazgos"] for r in resultados_estaticos)
    
    print(f"Archivos analizados por Bandit y Ruff: {total_archivos}")
    print(f"Archivos con 0 vulnerabilidades: {total_limpios} / {total_archivos}")
    print(f"Total hallazgos de seguridad: {total_hallazgos}")
    print("=" * 80)

if __name__ == "__main__":
    main()

