#!/usr/bin/env python3
"""
Script de Pruebas de Humo (Smoke Tests - 6/6)
Proyecto: TecnoAula — Triaje Automático de Solicitudes de Soporte (Caso 03 · Grupo 3 UNIANDES)
Uso:
  python tests/smoke.py [URL_BASE]
  Por defecto prueba local (http://localhost:8000) o la URL pública de Azure si se pasa como argumento.
"""

import sys
import json
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Forzar salida UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

URL_BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost:8000"

def hacer_peticion(metodo: str, endpoint: str, body: dict = None) -> tuple:
    url = f"{URL_BASE}{endpoint}"
    data = json.dumps(body).encode("utf-8") if body else None
    headers = {"Content-Type": "application/json"}
    req = Request(url, data=data, headers=headers, method=metodo)
    try:
        t0 = time.time()
        with urlopen(req, timeout=25) as res:
            duracion = (time.time() - t0) * 1000
            res_body = res.read().decode("utf-8")
            return res.status, json.loads(res_body) if res_body else {}, duracion
    except HTTPError as e:
        res_body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(res_body), 0.0
        except Exception:
            return e.code, {"error": res_body}, 0.0
    except URLError as e:
        return 0, {"error": str(e.reason)}, 0.0
    except Exception as e:
        return 0, {"error": str(e)}, 0.0


def main():
    print(f"\n=======================================================")
    print(f"INICIANDO SMOKE TESTS (6/6) EN: {URL_BASE}")
    print(f"=======================================================\n")

    pruebas_pasadas = 0
    total_pruebas = 6

    # 1. Health Check
    print("1/6 Verificando Endpoint de Salud (/v1/salud o /health)...", end=" ")
    status, body, ms = hacer_peticion("GET", "/v1/salud")
    if status != 200:
        status, body, ms = hacer_peticion("GET", "/health")
    if status == 200:
        print(f"[OK] PASÓ (200 OK · {ms:.1f}ms)")
        pruebas_pasadas += 1
    else:
        print(f"[ERROR] FALLÓ (Status {status}: {body})")

    # 2. Clasificación de Incidente Técnico
    print("2/6 Clasificación de Incidente Técnico...", end=" ")
    payload_incidente = {
        "nombre_cliente": "Colaborador Auditor",
        "email_cliente": "auditor@empresa.com",
        "descripcion_problema": "Olvidé mi contraseña de Windows y mi usuario en Active Directory está bloqueado tras 5 intentos fallidos."
    }
    status, body, ms = hacer_peticion("POST", "/clasificar", payload_incidente)
    if status != 201:
        status, body, ms = hacer_peticion("POST", "/v1/tickets/clasificar", payload_incidente)
    if status == 201 and "prioridad" in body:
        print(f"[OK] PASÓ (201 Created · Código: {body.get('ticket_codigo', 'OK')} · {ms:.1f}ms)")
        pruebas_pasadas += 1
    else:
        print(f"[ERROR] FALLÓ (Status {status}: {body})")

    # 3. Recuperación RAG con Citas Verificables
    print("3/6 Recuperación RAG sobre 15 Manuales Oficiales...", end=" ")
    if status == 201 and body.get("citas") and len(body["citas"]) > 0:
        doc = body["citas"][0].get("documento_id")
        print(f"[OK] PASÓ (Cita oficial: {doc} · {ms:.1f}ms)")
        pruebas_pasadas += 1
    else:
        print(f"[ERROR] FALLÓ (Sin citas verificables)")

    # 4. Cálculo Determinista de Prioridad ITIL (0 tokens)
    print("4/6 Cálculo Determinista ITIL (Prioridad y SLA)...", end=" ")
    if status == 201 and body.get("prioridad") in ["Alta", "Media", "Baja"] and body.get("sla_minutos", 0) > 0:
        print(f"[OK] PASÓ (Prioridad: {body['prioridad']} · SLA: {body['sla_minutos']} min)")
        pruebas_pasadas += 1
    else:
        print(f"[ERROR] FALLÓ (Prioridad o SLA no conforme a matriz determinista)")

    # 5. Regla de Silencio y Abstención (Zero-Hallucination)
    print("5/6 Protocolo de Silencio y Abstención Fuera de Alcance...", end=" ")
    payload_fuera = {
        "nombre_cliente": "Colaborador",
        "email_cliente": "personal@empresa.com",
        "descripcion_problema": "¿Cuál es la receta del ceviche de camarón o el menú del almuerzo?"
    }
    status_f, body_f, ms_f = hacer_peticion("POST", "/clasificar", payload_fuera)
    if status_f != 201:
        status_f, body_f, ms_f = hacer_peticion("POST", "/v1/tickets/clasificar", payload_fuera)
    if status_f == 201 and len(body_f.get("citas", [])) == 0 and "orientación" in body_f.get("solucion_propuesta", "").lower():
        print(f"[OK] PASÓ (Abstención estricta: 0 citas alucinadas)")
        pruebas_pasadas += 1
    else:
        print(f"[ERROR] FALLÓ (No aplicó regla de silencio)")

    # 6. Resiliencia, Fallback y Failover
    print("6/6 Resiliencia y Conmutación Transparente (Groq/Offline)...", end=" ")
    payload_caida = {
        "nombre_cliente": "Prueba Chaos",
        "email_cliente": "chaos@empresa.com",
        "descripcion_problema": "La impresora del departamento contable tiene un atasco de papel en la bandeja 2.",
        "simular_caida_gemini": True
    }
    status_c, body_c, ms_c = hacer_peticion("POST", "/clasificar", payload_caida)
    if status_c != 201:
        status_c, body_c, ms_c = hacer_peticion("POST", "/v1/tickets/clasificar", payload_caida)
    if status_c == 201 and body_c.get("metadatos_ia", {}).get("conmutado") is True:
        prov = body_c["metadatos_ia"]["proveedor"]
        print(f"[OK] PASÓ (Conmutado exitosamente a: {prov})")
        pruebas_pasadas += 1
    else:
        print(f"[ERROR] FALLÓ (No se registró la conmutación transparente)")

    print(f"\n=======================================================")
    print(f"RESULTADO SMOKE TESTS: {pruebas_pasadas}/{total_pruebas} APROBADAS")
    print(f"=======================================================\n")
    if pruebas_pasadas == total_pruebas:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()

