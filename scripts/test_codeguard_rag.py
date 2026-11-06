import urllib.request
import json

payload = {
    "archivo": "app/services/sanitizador_lopdp.py",
    "codigo": """import re

PATRON_PASSWORD = re.compile(
    r'(?i)(?:password|clave|token|secreto)\\s*[:=]\\s*([^\\s,;]+)'
)

def anonimizar_datos_sensibles(texto: str) -> str:
    \"\"\"Neutraliza contraseñas según LOPDP antes de enviar al LLM.\"\"\"
    if not texto:
        return ""
    return PATRON_PASSWORD.sub("clave: [CONFIDENCIAL_REMOVIDO]", texto)
"""
}

req = urllib.request.Request(
    "https://revisor-inteligente-codigo-production.up.railway.app/api/v1/analizar",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print("Status:", resp.status)
        print("Hallazgos de IA (Vulnerabilidades):", res.get("hallazgos"))
        print("Herramientas Estáticas:", res.get("analisis_estatico", {}).get("herramientas"))
        print("Fuentes RAG consultadas:", [f["documento"] + " - " + f["seccion"] for f in res.get("fuentes", [])])
except Exception as e:
    print("Error:", e)

