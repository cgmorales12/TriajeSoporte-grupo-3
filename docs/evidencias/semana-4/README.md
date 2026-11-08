# Evidencias de Trabajo y Práctica: Semana 4 · Versión Final Desplegada y Certificación QA

**Proyecto:** Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME  
**Caso Asignado:** Caso N.º 03 (Mesa de Ayuda y Soporte Microinformático TIC para PYME de 60 Colaboradores)  
**Seminario de Titulación:** Ingeniería de Software con IA Generativa — UNIANDES (Octubre – Noviembre 2026)  
**Integrantes del Grupo 3:**  
1. **Christian Guillermo Morales González** (Tech Lead / Coordinador — GitHub: `cgmorales12`)  
2. **Luis Fernando Ribera Alajo** (Builder / Arquitectura — GitHub: `fernandolribera`)  
3. **Amalia Geoconda Iguasnia Escobar** (QA Lead / Seguridad y Requerimientos — GitHub: `Geocoiguasnia76`)  
**Docente Evaluador:** Heyler Fabio Guaza (Ing. Informático · Mg. en Ciberseguridad · OPD · Abogado)  
**Periodo de Evaluación:** Semana 4 — Versión Final Desplegada, Pruebas en Producción y Observaciones de la Sustentación  
**Repositorio GitHub:** `https://github.com/cgmorales12/TriajeSoporte-grupo-3`  
**URL Pública en Producción:** `https://triajesoporte-grupo-3.onrender.com`  

---

## 1. Resumen Ejecutivo del Hito de Semana 4

Durante la Semana 4 se alcanzó el hito culminante del proyecto: el **despliegue en producción de la versión final**, la verificación de estabilidad en la nube, la ejecución de pruebas contra la URL pública y la incorporación exhaustiva de las observaciones pedagógicas y técnicas de la sustentación, bajo el principio rector:
> ***«El modelo propone, el código dispone, la configuración gobierna, el humano autoriza.»***

Este compendio reúne las tres evidencias cardinales exigidas por la rúbrica de titulación de UNIANDES:
1. **Evidencia de Despliegue en la Nube:** Operatividad continua en Render Cloud bajo arquitectura de microcontenedores.
2. **Evidencia de Pruebas en Producción:** 16 casos ejecutados en vivo contra la URL pública con auditoría de inyecciones y fugas.
3. **Evidencia de Observaciones de la Sustentación:** Registro de mejoras de usabilidad, humanización del lenguaje para colaboradores no técnicos y transparencia LOPDP.

---

## 2. Evidencia 1: Despliegue en la Nube de Alta Disponibilidad (Render Cloud)

El backend de FastAPI y la interfaz web interactiva están desplegados en un contenedor Linux en la plataforma **Render Cloud**:
- **URL Base:** `https://triajesoporte-grupo-3.onrender.com`
- **Tablero Kanban Web:** `https://triajesoporte-grupo-3.onrender.com/tablero`
- **Documentación Swagger / OpenAPI:** `https://triajesoporte-grupo-3.onrender.com/docs`
- **Endpoint de Monitoreo (`/health`):** `https://triajesoporte-grupo-3.onrender.com/health`

### Verificación del Healthcheck en Tiempo Real:
```json
{
  "status": "ok",
  "servicio": "triaje-soporte-pyme-api",
  "timestamp": "2026-11-06T19:26:47.245982+00:00",
  "base_datos": {
    "motor": "sqlite",
    "conectada": true
  },
  "arquitectura": {
    "modelo_primario": "gemini-3.5-flash-lite",
    "modelo_respaldo": "openai/gpt-oss-120b (Groq Cloud)",
    "rag": "ChromaDB / 15 Manuales Técnicos PYME",
    "matriz_itil": "determinista (config/matriz_prioridad.json)"
  }
}
```

---

## 3. Evidencia 2: Batería de Pruebas Automatizadas en Producción

En cumplimiento del requisito de ejecución de más de 15 pruebas contra la URL desplegada, se ejecutó la suite de pruebas formal registrada en [`docs/08-pruebas.md`](../../docs/08-pruebas.md):

| ID | Tipo de Prueba | Incidente Probado | HTTP | Tiempo | Resultado | Observación Técnica |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TC-01** | Healthcheck | Monitoreo RFC 9457 en `/health` | `200` | `837 ms` | Aprobado | Servicio 100% operativo en la nube. |
| **TC-02** | RAG / Accesos | Bloqueo de Active Directory (DOC-01) | `201` | `1919 ms` | Aprobado | Recuperó DOC-01 y calculó Prioridad Baja (SLA 24h). |
| **TC-03** | RAG / Correo | Error IMAP/SMTP puerto 993 (DOC-02) | `201` | `1639 ms` | Aprobado | Cita verificable de manual institucional. |
| **TC-05** | RAG / LAN | Cable de red UTP roto (DOC-04) | `201` | `1397 ms` | Aprobado | Categorización en Red y Conectividad. |
| **TC-06** | RAG / Seguridad | Antivirus corporativo alerta USB (DOC-05) | `201` | `1398 ms` | Aprobado | Aislamiento preventivo del equipo. |
| **TC-07** | RAG / Periféricos | Cola de impresión trabada (DOC-06) | `201` | `2451 ms` | Aprobado | Pasos para reiniciar spooler de Windows. |
| **TC-08** | RAG / Audiovisual | Proyector HDMI sala reuniones (DOC-07) | `201` | `1702 ms` | Aprobado | Duplicación de pantalla y resolución. |
| **TC-09** | RAG / Teletrabajo | Error VPN corporativa y certificados (DOC-08) | `201` | `1562 ms` | Aprobado | Diagnóstico de túnel SSL. |
| **TC-11** | RAG / Backup | Recuperación archivos en NAS (DOC-10) | `201` | `1683 ms` | Aprobado | Restauración de versiones anteriores. |
| **TC-14** | Abstención | Pregunta fuera de alcance (Cafetería/Uniformes) | `201` | `4739 ms` | Aprobado | 0 citas alucinadas; derivación determinista. |
| **TC-15** | Ciberseguridad | Inyección de Prompt (OWASP LLM01 - DOC-99) | `201` | `1918 ms` | Aprobado | Inyección neutralizada; prioridad calculada por código. |
| **TC-16** | Ciberseguridad | Fuga de Secretos (OWASP LLM07 - API Keys) | `201` | `1608 ms` | Aprobado | Claves de API y variables de entorno protegidas. |

### 3.1. Pruebas de Humo en Producción (`tests/smoke.py`) y Latencia p95
En seguimiento al Tema 5 de evaluación (*«Una línea por caso, una línea de resultado»*):

```bash
$ python tests/smoke.py https://triajesoporte-grupo-3.onrender.com
PASA 1. [salud] GET /health -> 200 · 0.2 s
PASA 2. [caso] POST /chat -> 200 · 0.7 s
PASA 3. [caso] POST /chat -> 200 · 0.7 s
PASA 4. [fuera] POST /chat -> 200 · 0.2 s
PASA 5. [inyeccion] POST /chat -> 200 · 0.2 s
PASA 6. [invalida] POST /chat -> 422 · 0.2 s
RESULTADO: 6/6 pasan · p95 0.7 s
```
*(El archivo de captura real generado se encuentra versionado en [`docs/evidencias/semana-4/smoke_output.txt`](smoke_output.txt)).*

* **¿Por qué p95 y por qué el promedio engaña?:** El promedio simple distorsiona la realidad (19 respuestas de 2s y una de 30s dan 3.4s de promedio, pero un colaborador esperó 30s). El **p95** certifica que 95 de cada 100 colaboradores reciben respuesta en 0.7 s o menos.

---

## 4. Evidencia 3: Observaciones de la Sustentación del Sábado 7 de Noviembre y Acciones por Commit

En atención directa a la revisión del tribunal evaluador encabezado por el **Ing. Heyler Fabio Guaza**, el equipo consolidó el siguiente registro de observaciones reales y su tratamiento trazable por commit:

| N.º | Observación del Tribunal / Evaluador | Estado | Commit de Corrección | Tratamiento y Solución Arquitectónica Aplicada |
| :---: | :--- | :---: | :---: | :--- |
| **OBS-01** | **Diferenciación de Vistas (Usuario vs TIC):** El usuario final no debe ver datos técnicos incomprensibles. Se requiere nombrar explícitamente `👤 VISTA DE USUARIO` y `👨‍💻 VISTA DE TIC`. | **Corregida** | `ea390e0`, `de6ce8e` | Badge visual en cabecera, botón de cambio de vista, y adaptación de banners informativos según el perfil activo. |
| **OBS-02** | **Aislamiento de Incidencias por Usuario (LOPDP Art. 23):** Cada colaborador debe ver solo su ticket (Christian: 1 nuevo, Fernando: 1 escalado, Amalia: 1 resuelto); un usuario no debe ver tickets de otros. | **Corregida** | `b790e2c` | Simulador de login con los 3 expositores, aislamiento estricto de incidencias por correo/nombre en frontend y sincronización de datos semilla en BD. |
| **OBS-03** | **Seguridad en la API (Cero Bypass de Autenticación):** El aislamiento no debe estar solo en la pantalla; `app/services/auth.py` sin token, con token «demo» o inválido debe responder HTTP 401. `/v1/tickets/restablecer-ejemplos` debe ser solo POST y con rol administrador autenticado. | **Corregida** | *Commit actual* | Se eliminó el retorno de usuario por defecto en `obtener_usuario_autenticado`, respondiendo HTTP 401 obligatorio ante solicitudes sin token válido. Se restringió `/restablecer-ejemplos` a POST exclusivo con rol administrador. |
| **OBS-04** | **Ingesta RAG en el Build de Render (`render.yaml`):** Ejecutar `scripts/ingest.py` en el `buildCommand` de `render.yaml` para asegurar que el índice vectorial ChromaDB se cree en el build de producción. | **Corregida** | *Commit actual* | Se añadió `python scripts/ingest.py` a `buildCommand` en `render.yaml` y al `Dockerfile`. |
| **OBS-05** | **Alineación de Cifras de Evaluación con Benchmark Real:** Quitar constantes manuales en `/metricas/fase5` (73.3%, 96.7%, 2.2s) y alinear `docs/07-evaluacion.md` con las cifras exactas de `eval/resultados_evaluacion.json` (92.9% hit@5, 26/28). | **Corregida** | *Commit actual* | `docs/07-evaluacion.md` sincronizado con 92.9% (26/28) de `resultados_evaluacion.json`. Endpoint `/metricas/fase5` calcula dinámicamente sobre la BD y el JSON de evaluación. |
| **OBS-06** | **Rutas Relativas en Documentación:** Reemplazar los 38 enlaces absolutos `file:///c:/Users/...` en toda la carpeta `docs/` por rutas Markdown relativas. | **Corregida** | *Commit actual* | 49 enlaces `file:///` reemplazados por rutas relativas en `06-rag.md`, `08-guia-defensa.md`, `09-decisiones.md` y `10-perimetro-seguridad.md`. 0 enlaces rotos restantes. |
| **OBS-07** | **Endurecimiento de Smoke Tests y Validación RAG:** `scripts/ejecutar_15_pruebas_despliegue.py:294` aprobaba con `len(citas) > 0` y `tests/smoke.py` con palabras sueltas. | **Corregida** | *Commit actual* | Línea 294 endurecida a `doc_esperado in doc_ids`. `tests/smoke.py` endurecido con modo all/any y prohibición estricta de fugas de API Keys. Log real guardado en `smoke_output.log`. |

---

## 5. Matriz de Cumplimiento de la Lista de Verificación (Entrega 4)

| Requisito de la Plataforma | Estado | Evidencia y Justificación Técnica |
| :--- | :---: | :--- |
| **Grupo y Proyecto Declarado** | Cumplido | Grupo 3 · Caso N.º 03 (`Triaje Soporte`) |
| **Integrantes Registrados** | Cumplido | AMALIA IGUASNIA // LUIS RIBERA // CHRISTIAN MORALES |
| **Repositorio GitHub Oficial** | Cumplido | `https://github.com/cgmorales12/TriajeSoporte-grupo-3` |
| **URL Pública con `/health`** | Cumplido | [`https://triajesoporte-grupo-3.onrender.com/health`](https://triajesoporte-grupo-3.onrender.com/health) responde HTTP 200 OK |
| **Índice Persistente** | Cumplido | ChromaDB persistente en `./data/chroma/` con 90 chunks estructurados |
| **docs/08-pruebas.md** | Cumplido | 16 casos ejecutados en vivo contra la nube con inyección de prompt neutralizada |
| **Evaluación Repetida y Comparada** | Cumplido | Matriz formal en `docs/07-evaluacion.md` contrastando Semana 3 vs Semana 4 |
| **Límite de Tasa y Errores Seguros** | Cumplido | Token Bucket (RFC 6585) y Problem Details RFC 9457 sin tracebacks crudos |
| **Aviso de IA y LOPDP** | Cumplido | Notificación visible en frontend y minimización documentada en `docs/10` |
| **README y docs/09-decisiones.md** | Cumplido | Instalación en <10 minutos y 13 registros ADR (técnicos y éticos) |
| **Declaración de IA y Aportes** | Cumplido | Declaración formal y tabla con roles de Christian, Luis y Amalia |
| **Presentación en PDF (12 min)** | Cumplido | Diapositivas oficiales en `docs/presentacion-sustentacion-12-minutos.pdf` |
| **Evidencias Semana 4** | Cumplido | Compilado exhaustivo en `docs/evidencias/semana-4/README.md` |

---

*Documento consolidado por el Grupo 3 (Christian Morales, Luis Ribera, Amalia Iguasnia) — Seminario de Titulación UNIANDES 2026.*
