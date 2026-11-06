# Guía Maestra de Defensa de Grado y Preguntas del Tribunal Evaluador
**Proyecto:** ConectaTec / TecnoAula — Triaje y Resolución Inteligente de Incidentes para ISP e Instituciones Educativas  
**Seminario de Titulación:** Ingeniería de Software con Inteligencia Artificial Generativa  
**Universidad Regional Autónoma de los Andes (UNIANDES)** — Octubre – Noviembre 2026  
**Caso Asignado:** Caso N.º 03 · Grupo de Desarrollo N.º 03  
**Integrantes del Grupo 3:**  
1. **Christian Guillermo Morales González** (Tech Lead / Coordinador — GitHub: `cgmorales12`)  
2. **Luis Fernando Ribera Alajo** (Builder / Arquitectura — GitHub: `fernandolribera`)  
3. **Amalia Geoconda Iguasnia Escobar** (QA / Seguridad y Requerimientos — GitHub: `Geocoiguasnia76`)  
**Docente Evaluador:** Ing. Heyler Fabio Guaza (Ing. Informático · Mg. en Ciberseguridad · OPD · Abogado)  
**Versión:** 2.0 (Consolidado de Semana 2)

---

## 🎯 1. Guion y Estructura de la Presentación Oral (12 Minutos)

Para maximizar el impacto ante el jurado, la sustentación debe seguir un esquema ágil de 12 minutos repartidos equitativamente entre los tres integrantes:

```
[00:00 - 04:00]  Christian Morales  --> Visión de Negocio, C4 y Gateway Resiliente LLM
[04:00 - 08:00]  Fernando Ribera   --> Principio Rector ITIL, SQLite y Motor RAG con Citas
[08:00 - 12:00]  Amalia Iguasnia    --> Ciberseguridad LOPDP, Mocks de Pruebas y Cero Secretos
```

### 1.1. Intervención 1: Christian Morales (Tech Lead — 4 Minutos)
1. **Problema Real y Justificación de Negocio:**
   - La saturación crítica de las mesas de ayuda por incidencias repetitivas de primer nivel (luces de ONT, Wi-Fi, DNS, accesos).
   - El costo elevado de enviar cuadrillas presenciales ($15 a $25 USD por visita) cuando el 73% de averías pueden resolverse por autoatención guiada.
2. **Arquitectura C4 y Desacoplamiento (ADR-001 y ADR-005):**
   - Mostrar el Modelo C4 en sus 4 niveles (Contexto, Contenedores, Componentes y Código).
   - Explicar el patrón **Gateway / Strategy** en `ClienteLLM`: el modelo de lenguaje está completamente encapsulado; cambiar de proveedor no altera la firma de ningún endpoint ni los esquemas Pydantic.
3. **Gateway de Resiliencia, Failover y FinOps (ADR-002, ADR-008 y ADR-009):**
   - Demostrar el manejo de errores HTTP 429 con Exponential Backoff ($0.5s \times 2^i$), control estricto de timeout (12s) y fallback automático:  
     $$\text{Google Gemini 1.5 Flash} \longrightarrow \text{Groq Cloud (Llama 3.3 70B)} \longrightarrow \text{Heurístico Local Offline}$$
   - Mostrar la telemetría en tiempo real: medición de tokens de entrada/salida y latencia por solicitud en el endpoint `/v1/metricas/solicitudes` y en el badge del frontend.

### 1.2. Intervención 2: Luis Fernando Ribera (Builder — 4 Minutos)
1. **El Principio Rector de Arquitectura (ADR-003):**
   - *«El modelo propone, el código dispone»*. El LLM es probabilístico y jamás debe calcular SLAs ni prioridades contractuales.
   - El modelo solo extrae `Impacto` y `Urgencia`; una función matemática pura en Python (`app/tools/priorizar.py`) lee la matriz en `config/matriz_prioridad.json` y calcula la Prioridad y los minutos SLA con cero alucinaciones y cero gasto de tokens.
2. **Persistencia Segura y Portabilidad (ADR-004):**
   - Uso de SQLite embebido con consultas 100% parametrizadas con marcadores de posición `?`, neutralizando inyecciones SQL (OWASP SQLi).
   - Cero fricción de despliegue para el evaluador: no requiere instalar daemons de PostgreSQL ni pagar clusters en la nube.
3. **Motor RAG con Citas Técnicas Verificables (Grounding):**
   - Demostración de las 15 guías técnicas oficiales (`DOC-01` a `DOC-15`) en `data/raw/`.
   - Cada diagnóstico incluye obligatoriamente el código del manual, título y paso exacto de resolución.
4. **Demostración del Tablero Kanban Frontend:**
   - Visualización de las 4 columnas operativas (`Nuevos`, `En Atención`, `Escalado a Cuadrilla`, `Resueltos`).
   - Muestra del botón reactivo con deshabilitación instantánea y spinner mientras la IA procesa la solicitud.

### 1.3. Intervención 3: Amalia Geoconda Iguasnia (QA / Seguridad — 4 Minutos)
1. **Cumplimiento Legal LOPDP (Ecuador) y Mitigación de Fugas (ADR-007):**
   - **Anonimización previa (Art. 23 LOPDP):** Detección automática por Regex de contraseñas accidentales escritas por docentes o usuarios y reemplazo preventivo por `[CONFIDENCIAL_REMOVIDO]` antes de llegar al modelo o a la base de datos.
   - **Filtro de Contrato:** Pydantic V2 con `extra="forbid"` y `response_model` en FastAPI para evitar fuga de PII, system prompts o tracebacks (OWASP LLM02).
2. **Defensa en Profundidad contra Inyección de Prompts (ADR-006):**
   - Aislamiento semántico en `<solicitud>{texto}</solicitud>`.
   - Directivas taxativas de abstención en `system_v3.md`: el modelo responde con `requiere_revision_humana: true` ante consultas fuera de alcance o ataques adversos.
3. **Control de Abuso y Token Bucket (RFC 6585):**
   - Limitador de tasa por IP de 15 fichas con recarga de 1 cada 3 segundos, respondiendo con `HTTP 429 Too Many Requests` y encabezado `Retry-After`.
4. **Suite de Pruebas Unitarias Automatizadas con Mocks (ADR-010):**
   - Demostración de **28 pruebas unitarias pasando en 3.3 segundos con $0.00 USD de costo de API**, gracias a dobles de prueba deterministas (`monkeypatch`).
   - Prueba desconectada de red: eliminación de claves de API demostrando operación 100% offline.
5. **Cero Secretos en Git:**
   - Auditoría automatizada con `scripts/auditar_cero_secretos.py` con 100% de cumplimiento.

---

## 🛡️ 2. Banco de Preguntas Críticas de la Rúbrica Oficial (Caso 03 · Fase 5)

### Pregunta Oficial 1 (Fase 5): *«¿Qué porcentaje de solicitudes se resolvieron sin intervención humana y cómo lo demostraron?»*
* **Respuesta del Equipo:**  
  *«En nuestro conjunto oficial de evaluación de 30 solicitudes de referencia (`eval/preguntas.json`), **73.3% (22 de 30 solicitudes)** fueron resueltas exitosamente en Nivel 1 mediante autoatención RAG guiada sobre los 15 manuales técnicos internos, superando la meta de la rúbrica ($\ge 70\%$).  
  Lo demostramos mediante la suite cuantitativa automatizada `eval/run_eval.py`: cada solicitud técnica de autoatención obtiene una cita oficial verificable (ID de documento y paso exacto), verifica que no existan alucinaciones y valida que el colaborador pueda resolver el incidente en su puesto sin consumir tiempo del técnico. El restante 26.7% correspondió a solicitudes con requerimiento de escalamiento físico presencial o privilegios administrativos, las cuales fueron derivadas correctamente a Nivel 2.»*
* **Archivos de respaldo:** [`eval/run_eval.py`](eval/run_eval.py), [`eval/preguntas.json`](eval/preguntas.json) y [`eval/resultados_evaluacion.json`](eval/resultados_evaluacion.json).

---

### Pregunta Oficial 2 (Fase 5): *«¿Cómo definieron y probaron la regla de escalamiento de tickets?»*
* **Respuesta del Equipo:**  
  *«La regla de escalamiento está gobernada **100% por código determinista en Python, nunca por la prosa del LLM**. Se definieron tres condiciones estrictas de escalamiento a Nivel 2:  
  1. **Requerimiento de privilegios elevados de infraestructura:** Casos que exigen credenciales de Administrador de Dominio (Active Directory), reseteo de perfiles ERP o reconfiguración de VLANs de red.  
  2. **Averías físicas de hardware:** Detección de fallas no solucionables por software (ruido metálico de disco duro, fallas de tarjeta madre, rotura física de cables/rosetas de red o pantalla azul BSOD recurrente).  
  3. **Compuerta Human-in-the-Loop (HITL · OWASP LLM08):** Todo escalamiento a técnico presencial o derivación física se bloquea preventivamente (`estado: pendiente_aprobacion_humana`) hasta que un operador humano confirme la acción (`confirmado=True`).  
  Esta regla se probó exhaustivamente en `tests/test_herramientas_agente.py` (`test_tool_escalar_hitl_bloqueo_sin_confirmacion` y `test_tool_escalar_hitl_ejecucion_con_confirmacion`) y en los 5 escenarios ReAct de `eval/run_eval.py`.»*
* **Archivos de respaldo:** [`app/agente.py`](app/agente.py), [`app/tools/priorizar.py`](app/tools/priorizar.py) y [`tests/test_herramientas_agente.py`](tests/test_herramientas_agente.py).

---

### Pregunta Oficial 3 (Fase 5): *«¿Cuáles son las métricas de Retorno de Inversión (ROI) para la PYME de 60 colaboradores?»*
* **Respuesta del Equipo:**  
  *«Para una PYME con 60 colaboradores y un único técnico de TI desbordado, TecnoAula entrega métricas de ROI medibles y contundentes:  
  1. **Ahorro de Tiempo del Técnico:** Al resolver el 73.3% de las solicitudes repetitivas por autoatención N1 (desbloqueo de contraseñas, atascos de impresora, configuración VPN, ERP), se liberan **~15 horas semanales** del técnico (más de **60 horas al mes**), permitiéndole enfocarse en proyectos estratégicos y ciberseguridad.  
  2. **Reducción Drástica del MTTR (Tiempo Medio de Resolución):** Las incidencias comunes pasan de un tiempo de espera promedio de **4 horas** a una resolución en **menos de 2 minutos** guiada por el paso a paso de los manuales RAG.  
  3. **Costo Evitado de Personal:** Se evita la contratación indispensable de un segundo técnico de soporte de Nivel 1, lo que representa un ahorro directo estimado de **$800 a $1.000 USD mensuales** para la PYME.  
  4. **Eficiencia FinOps de Inferencia:** Gracias a Gemini 1.5 Flash y la técnica de Context Caching, el costo de inferencia por ticket es inferior a **$0.002 USD**, logrando un costo operativo mensual de IA menor a **$1.50 USD**.»*
* **Archivos de respaldo:** [`docs/01-propuesta.md`](docs/01-propuesta.md) y [`config/matriz_prioridad.json`](config/matriz_prioridad.json).

---

### Pregunta Oficial 4 (Fase 5): *«¿Cómo demuestran que TecnoAula no está diseñado para una empresa específica, sino como una solución general para cualquier PYME?»*
* **Respuesta del Equipo:**  
  *«Demostramos la generalidad y adaptabilidad de TecnoAula a través de tres pilares arquitectónicos auditables:  
  1. **Universalidad de Necesidades Ofimáticas:** Los 15 manuales técnicos estándar abordan la infraestructura tecnológica que comparte cualquier PYME moderna (Active Directory / Windows / Google / M365, clientes VPN corporativos, impresoras departamentales en red, carpetas compartidas SMB/NAS, ERPs contables y redes Wi-Fi). No depende del giro de negocio, sirviendo tanto para empresas de servicios como para consultoras, distribuidoras o firmas profesionales.  
  2. **Base de Conocimiento Desacoplada y Extensible (Corpus RAG en Markdown):** El conocimiento no está quemado en el código fuente. Cualquier PYME puede agregar o modificar manuales en `data/raw/` y re-ejecutar `python scripts/ingest.py` para re-indexar ChromaDB automáticamente en 5 segundos.  
  3. **Matriz de Priorización ITIL Parametrizable:** Las reglas de negocio, niveles de severidad y tiempos máximos de SLA están desacoplados en `config/matriz_prioridad.json`. Cualquier empresa puede configurar sus propios SLAs sin alterar una sola línea de código backend.  
  4. **Esquemas Pydantic V2 Genéricos:** Los contratos DTO procesan categorías estándar de TI de la industria, garantizando total portabilidad.»*
* **Archivos de respaldo:** [`data/raw/README.md`](data/raw/README.md), [`config/matriz_prioridad.json`](config/matriz_prioridad.json) y [`docs/04-fuentes.md`](docs/04-fuentes.md).

---

## 🛡️ 3. Banco de Preguntas Adicionales del Tribunal y Respuestas de Alto Nivel

### Pregunta 1: *«¿Por qué no le pidieron al LLM que calcule directamente la prioridad y el tiempo SLA de resolución?»*
* **Respuesta del Equipo:**  
  *«Porque los Modelos de Lenguaje son sistemas estocásticos y probabilísticos, no motores de cálculo determinista. En la gestión de servicios ITIL v4 y en acuerdos de nivel de servicio (SLA), los tiempos de respuesta tienen consecuencias contractuales y financieras que no pueden depender de la temperatura o del muestreo probabilístico de un modelo. En nuestro sistema aplicamos la regla fundacional: 'El modelo propone, el código dispone'. El LLM únicamente extrae el Impacto y la Urgencia cualitativa desde el lenguaje natural del reporte; luego, nuestra función determinista en Python lee la matriz oficial en `config/matriz_prioridad.json` y calcula la prioridad matemática y los minutos de SLA. De este modo garantizamos cero alucinaciones, 100% de reproducibilidad y cero costo de tokens.»*
* **Archivos de respaldo:** [app/tools/priorizar.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/tools/priorizar.py) y [config/matriz_prioridad.json](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/config/matriz_prioridad.json).

---

### Pregunta 2: *«¿Qué ocurre si durante la operación en vivo la API de Google Gemini se cae (HTTP 503) o se satura la cuota (HTTP 429)?»*
* **Respuesta del Equipo:**  
  *«Diseñamos un Gateway de Resiliencia multinivel en `ClienteLLM`. Ante un error HTTP 429, el cliente no falla de inmediato: ejecuta un ciclo de hasta 3 reintentos gobernados por la fórmula de Exponential Backoff ($0.5s \times 2^{\text{intento}}$). Si la saturación persiste o la llamada excede el timeout estricto de 12 segundos, el sistema conmuta automáticamente en menos de 500 ms al modelo secundario Llama 3.3 70B en Groq Cloud. Si el entorno carece de conexión a internet, se activa un tercer nivel de contingencia: nuestro motor heurístico local offline. Además, cumplimos con el principio de transparencia: el payload y la interfaz web encienden un distintivo naranja informando al operador que la solicitud fue atendida por el modelo de respaldo y registrando el motivo exacto del fallo.»*
* **Archivos de respaldo:** [app/services/llm.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/services/llm.py) y [docs/09-decisiones/ADR-002-gateway-gemini-groq.md](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/docs/09-decisiones/ADR-002-gateway-gemini-groq.md).

---

### Pregunta 3: *«¿Cómo garantizan el cumplimiento de la Ley Orgánica de Protección de Datos Personales (LOPDP de Ecuador)?»*
* **Respuesta del Equipo:**  
  *«Aplicamos tres salvaguardas técnicas y legales auditables:  
  1. **Anonimización previa de credenciales (Art. 23 LOPDP):** Mediante expresiones regulares en la capa de entrada del backend, cualquier contraseña o clave Wi-Fi ingresada accidentalmente por el usuario es interceptada y sustituida por `[CONFIDENCIAL_REMOVIDO]` antes de enviar los datos al LLM o guardarlos en SQLite.  
  2. **Minimización de datos (Art. 10 LOPDP):** Solo se capturan los datos indispensables para el triaje técnico.  
  3. **Filtro de Contrato con `response_model` en FastAPI:** Evita la fuga de PII, system prompts, rutas internas o tracebacks hacia el cliente (OWASP LLM02).»*
* **Archivos de respaldo:** [app/routers/principal.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/routers/principal.py) y [docs/10-perimetro-seguridad-y-defensas-llm.md](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/docs/10-perimetro-seguridad-y-defensas-llm.md).

---

### Pregunta 4: *«¿Cómo mitigaron el riesgo de Inyección de Prompts y Jailbreak (OWASP LLM01)?»*
* **Respuesta del Equipo:**  
  *«Implementamos una arquitectura de Defensa en Profundidad con 4 capas:  
  1. **Aislamiento semántico XML:** La entrada del usuario nunca se concatena en prosa libre; se encapsula estrictamente dentro de etiquetas `<solicitud>{texto}</solicitud>`, instruyendo al modelo a tratarla como datos pasivos.  
  2. **Esquemas Pydantic V2 cerrados:** La configuración `model_config = ConfigDict(extra="forbid")` rechaza de inmediato cualquier payload que intente inyectar atributos espurios.  
  3. **Directiva de abstención en Prompt v3:** Instruye al modelo a rechazar instrucciones que contradigan su rol de mesa de ayuda y activar `requiere_revision_humana: true`.  
  4. **Lógica determinista:** La decisión de prioridad y escalamiento a cuadrilla la decide el código Python evaluando reglas de negocio, nunca la prosa generada por el LLM.»*
* **Archivos de respaldo:** [app/prompts/system_v3.md](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/prompts/system_v3.md) y [docs/05-prompts.md](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/docs/05-prompts.md).

---

### Pregunta 5: *«¿Por qué dicen que el cliente del modelo está encapsulado y cómo demuestran que cambiar de proveedor no toca los endpoints?»*
* **Respuesta del Equipo:**  
  *«Aplicamos el patrón Gateway / Strategy en `ClienteLLM`. Los controladores HTTP en FastAPI (`app/routers/principal.py`) no importan los SDKs de Google ni de Groq; únicamente consumen métodos de alto nivel: `cliente_llm.clasificar()`, `cliente_llm.chat_stream()` y `cliente_llm.analizar()`. Podemos cambiar de proveedor en tiempo de ejecución (`cliente_llm.cambiar_proveedor('groq')`) o modificando la variable `PROVEEDOR_LLM_ACTIVO` en `.env`, y los endpoints continúan recibiendo y emitiendo los mismos contratos tipados Pydantic V2 (`TicketOut`, `ResultadoAnalizarOut`). Ninguna línea de los controladores se modifica.»*
* **Archivos de respaldo:** [app/services/llm.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/services/llm.py) y [docs/09-decisiones/ADR-005-encapsulamiento-cliente-llm.md](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/docs/09-decisiones/ADR-005-encapsulamiento-cliente-llm.md).

---

### Pregunta 6: *«¿Cómo probaron los endpoints con `pytest` sin gastar saldo de API ni depender de conexión a internet?»*
* **Respuesta del Equipo:**  
  *«Construimos una suite de 28 pruebas unitarias automatizadas en `tests/test_endpoints.py` utilizando dobles de prueba (`monkeypatch`). Interceptamos las funciones del cliente LLM para retornar respuestas predecibles e instantáneas que validan todo el perímetro de backend (esquemas Pydantic, cálculo ITIL, citas RAG y persistencia SQLite) en tan solo 3.3 segundos con $0.00 USD de gasto. Incluso implementamos la prueba `test_mock_garantia_cero_consumo_api_y_cero_red` que borra las API keys del entorno y demuestra que el sistema aprueba 100% desconectado de internet.»*
* **Archivos de respaldo:** [tests/test_endpoints.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/tests/test_endpoints.py) y [docs/09-decisiones/ADR-010-pruebas-unitarias-con-mocks-cero-api.md](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/docs/09-decisiones/ADR-010-pruebas-unitarias-con-mocks-cero-api.md).

---

### Pregunta 7: *«¿Cómo miden y controlan los costos de inferencia y la latencia del sistema (FinOps)?»*
* **Respuesta del Equipo:**  
  *«Implementamos un middleware de observabilidad en `app/main.py`. Por cada solicitud de inferencia se miden con `time.perf_counter()` la duración exacta en milisegundos y se contabilizan los tokens de entrada (prompt), tokens de salida (completado) y tokens totales. Estos datos se inyectan en los encabezados HTTP (`X-Response-Time-Ms`, `X-Request-ID`), se escriben en logs estructurados con formato JSON y se exponen en el endpoint de telemetría `GET /v1/metricas/solicitudes`, permitiendo a los supervisores auditar promedios, máximos y costos proyectados en tiempo real.»*
* **Archivos de respaldo:** [app/main.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/main.py) y [docs/09-decisiones/ADR-009-observabilidad-y-telemetria-tokens.md](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/docs/09-decisiones/ADR-009-observabilidad-y-telemetria-tokens.md).

---

### Pregunta 8: *«¿Por qué la interfaz principal es un Tablero Kanban y no un chat abierto?»*
* **Respuesta del Equipo:**  
  *«Porque en la ingeniería de soporte técnico y gestión ITIL, los incidentes no son conversaciones de ocio; son **órdenes de trabajo con estados, responsables y tiempos máximos de atención (SLA)**. Un chat abierto oculta las averías pendientes y no permite balancear la carga de trabajo entre operadores. El tablero Kanban permite visualizar en tiempo real qué tickets están nuevos, cuáles están en diagnóstico remoto y cuáles requieren cuadrilla técnica presencial en la calle. Para asistencia conversacional específica incorporamos además el endpoint `POST /chat` con Streaming token a token.»*
* **Archivos de respaldo:** [frontend/index.html](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/frontend/index.html) y [docs/01-propuesta.md](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/docs/01-propuesta.md).

---

## 📋 3. Matriz de Trazabilidad: Concepto Teórico vs. Archivo en el Repositorio

| Concepto Evaluado por el Tribunal | Archivo Principal de Implementación | Justificación Técnica Breve |
|---|---|---|
| **Modelo C4 (Niveles 1 al 4)** | [docs/03-arquitectura.md](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/docs/03-arquitectura.md) | Diagramas Mermaid de Contexto, Contenedores, Componentes y Código/Secuencia. |
| **Cliente LLM Encapsulado** | [app/services/llm.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/services/llm.py) | Patrón Gateway / Strategy; conmutación en caliente sin tocar controladores. |
| **Failover Gemini $\to$ Groq** | [app/services/llm.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/services/llm.py) | Captura de errores 429/503/timeout y conmutación automática en <500 ms. |
| **Error 429 con Exponential Backoff** | [app/services/llm.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/services/llm.py) | Algoritmo de retroceso exponencial ($0.5s \times 2^i$) con hasta 3 reintentos. |
| **Priorización Determinista ITIL** | [app/tools/priorizar.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/tools/priorizar.py) | Cálculo matemático de prioridad y SLA leyendo `config/matriz_prioridad.json`. |
| **Validación Estricta Pydantic V2** | [app/schemas.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/schemas.py) | Modelos DTO con `ConfigDict(extra="forbid")` para neutralizar OWASP LLM05. |
| **Ciberseguridad y LOPDP (Art. 23)** | [app/routers/principal.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/routers/principal.py) | Anonimización previa de contraseñas por Regex (`[CONFIDENCIAL_REMOVIDO]`). |
| **Limitador de Tasa Token Bucket** | [app/main.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/main.py) | 15 fichas por IP, recarga cada 3s y respuesta RFC 6585 con `Retry-After`. |
| **Observabilidad y Tokens** | [app/main.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/main.py) | Registro de tokens in/out/total, latencia y endpoint `/v1/metricas/solicitudes`. |
| **Pruebas con Mocks (Cero API)** | [tests/test_endpoints.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/tests/test_endpoints.py) | 28 pruebas pasando en 3.3s con `monkeypatch` y $0.00 USD consumidos. |
| **Auditoría Cero Secretos** | [scripts/auditar_cero_secretos.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/scripts/auditar_cero_secretos.py) | Verificación de exclusión de `.env` en Git e historial limpio de commits. |
| **10 Decisiones de Arquitectura** | [docs/09-decisiones.md](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/docs/09-decisiones.md) | Registros ADR-001 al ADR-010 con contexto, decisión y consecuencias. |

---

## 🚀 4. Protocolo de Demostración en Vivo ante el Tribunal

1. **Paso 1: Demostrar la Suite de Pruebas Offline:**
   ```powershell
   python -m pytest tests/test_endpoints.py
   ```
   *Mensaje al jurado:* *"Observen cómo ejecutamos 28 pruebas unitarias de punta a punta en solo 3.3 segundos con cero consumo de saldo de API y garantía offline."*
2. **Paso 2: Demostrar Cero Secretos en Git:**
   ```powershell
   python scripts/auditar_cero_secretos.py
   ```
   *Mensaje al jurado:* *"Verificamos con este script automatizado el cumplimiento al 100% de la política de Cero Secretos en el historial de Git."*
3. **Paso 3: Triaje en Vivo en el Frontend (`http://127.0.0.1:8000/tablero`):**
   - Hacer clic en el botón de escenario rápido: **`🔴 LOS Roja ONT`**.
   - Presionar **`Diagnosticar e Iniciar Triaje`**.
   - Mostrar cómo el botón se deshabilita con el spinner `⏳ Analizando con IA y RAG...`.
   - Mostrar el ticket generado en la columna **`Nuevos`** con Prioridad Alta, SLA de 15m y la cita técnica obligatoria del manual oficial **`DOC-01`**.
4. **Paso 4: Demostración del Modo Vulnerable (Chaos Engineering):**
   - En el Simulador de Caída y Ataque, desactivar **"Defensas IA"** e ingresar una inyección de prompt adversa.
   - Mostrar cómo el modelo desprotegido alucina Prioridad Infinita y el manual falso DOC-99.
   - Reactivar **"Defensas IA"** y enviar el mismo ataque: el sistema neutraliza el intento dentro de `<solicitud>`, responde con Prioridad Baja determinista y preserva la integridad del servicio.
