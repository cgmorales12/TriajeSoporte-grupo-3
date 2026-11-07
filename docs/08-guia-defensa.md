# Guía Maestra de Defensa de Grado y Preguntas del Tribunal Evaluador
**Proyecto:** Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME (Caso N.º 03 · Grupo 3 UNIANDES)  
**Seminario de Titulación:** Ingeniería de Software con Inteligencia Artificial Generativa  
**Universidad Regional Autónoma de los Andes (UNIANDES)** — Octubre – Noviembre 2026  
**Caso Asignado:** Caso N.º 03 · Grupo de Desarrollo N.º 03  
**Integrantes del Grupo 3:**  
1. **Christian Guillermo Morales González** (Tech Lead / Coordinador — GitHub: `cgmorales12`)  
2. **Luis Fernando Ribera Alajo** (Builder / Arquitectura — GitHub: `fernandolribera`)  
3. **Amalia Geoconda Iguasnia Escobar** (QA / Seguridad y Requerimientos — GitHub: `Geocoiguasnia76`)  
**Docente Evaluador:** Ing. Heyler Fabio Guaza (Ing. Informático · Mg. en Ciberseguridad · OPD · Abogado)  
**Versión:** 4.0 (Consolidado Final de Titulación — Semana 4)

---

## 1. Guion y Estructura de la Presentación Oral (12 Minutos)

Para maximizar el impacto ante el jurado calificador, la sustentación sigue un esquema ágil de 12 minutos repartidos equitativamente entre los tres integrantes:

```
[00:00 - 04:00]  Christian Morales  --> Visión de Negocio PYME, Arquitectura C4 y Gateway Resiliente LLM
[04:00 - 08:00]  Fernando Ribera   --> Principio Rector ITIL, SQLite Parametrizado, RAG y Tablero Kanban
[08:00 - 12:00]  Amalia Iguasnia    --> Ciberseguridad LOPDP, 82 Pruebas Unitarias Mocks y Dashboard ROI (Fase 5)
```

### 1.1. Intervención 1: Christian Morales (Tech Lead — 4 Minutos)
1. **Problema Real y Justificación de Negocio en la PYME:**
   - Una empresa de servicios con **60 colaboradores** cuenta con **un único técnico de TI** desbordado por solicitudes repetitivas (bloqueo de claves en Active Directory, configuración de VPN FortiClient, atascos de impresora de red, carpetas compartidas en NAS y sesiones congeladas en el ERP contable).
   - El costo de atender estas incidencias de forma manual satura al técnico, impidiéndole atender la infraestructura crítica y la seguridad de la empresa.
2. **Arquitectura C4 y Desacoplamiento (ADR-001 y ADR-005):**
   - Mostrar el Modelo C4 en sus 4 niveles (Contexto, Contenedores, Componentes y Código).
   - Explicar el patrón **Gateway / Strategy** en `ClienteLLM`: el modelo de lenguaje está completamente encapsulado; cambiar de proveedor no altera la firma de ningún endpoint ni los contratos Pydantic V2 (`extra="forbid"`).
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
   - Explicación de dónde viven los datos: en el disco del contenedor Docker en Render (`/app/data/triaje_soporte.db`). Nace limpio y se puebla automáticamente con 20 tickets iniciales (5 por columna) gracias a `app/datos_semilla.py`.
3. **Motor RAG con Citas Técnicas Verificables (Grounding):**
   - Demostración de las 15 guías técnicas oficiales (`DOC-01` a `DOC-15`) en `data/raw/`.
   - Cada diagnóstico incluye obligatoriamente el código del manual, título y paso exacto de resolución (ej. `[DOC-01 · Paso 2]`).
4. **Demostración del Tablero Kanban Frontend:**
   - Visualización de las 4 columnas operativas (`Nuevos`, `En Atención`, `Escalado a Soporte Presencial`, `Resueltos`).
   - Muestra de los botones de prueba rápida (`🔑 Clave AD`, `🌐 VPN`, `🖨️ Impresora`, `📊 ERP`, `🖥️ Pantalla Azul`).

### 1.3. Intervención 3: Amalia Geoconda Iguasnia (QA / Seguridad — 4 Minutos)
1. **Cumplimiento Legal LOPDP (Ecuador) y Mitigación de Fugas (ADR-007):**
   - **Anonimización previa (Art. 23 LOPDP):** Detección automática por Regex de contraseñas accidentales escritas por colaboradores y reemplazo preventivo por `[CONFIDENCIAL_REMOVIDO]` antes de llegar al modelo o a la base de datos.
   - **Filtro de Contrato:** Pydantic V2 con `extra="forbid"` y `response_model` en FastAPI para evitar fuga de PII, system prompts o tracebacks (OWASP LLM02).
2. **Defensa en Profundidad contra Inyección de Prompts (ADR-006):**
   - Aislamiento semántico en `<solicitud>{texto}</solicitud>`.
   - Directivas taxativas de abstención en `system_v3.md`: el modelo responde con `requiere_revision_humana: true` ante consultas fuera de alcance o ataques adversos.
3. **Control de Abuso y Token Bucket (RFC 6585):**
   - Limitador de tasa por IP de 15 fichas con recarga de 1 cada 3 segundos, respondiendo con `HTTP 429 Too Many Requests` y encabezado `Retry-After`.
4. **Suite de Pruebas Unitarias Automatizadas con Mocks (ADR-010):**
   - Demostración de **82 pruebas unitarias pasando en segundos con $0.00 USD de costo de API**, gracias a dobles de prueba deterministas (`monkeypatch`).
   - Cero secretos en Git verificado con herramientas SAST y auditoría de Bandit.
5. **Dashboard de Métricas y Retorno de Inversión (Fase 5):**
   - Demostración en vivo en la Vista TIC del dashboard con la tasa de autoatención (73.3%), las compuertas de escalamiento y el ahorro anual proyectado (\$16,987 USD/año).
6. **Pruebas de Humo en Producción y Latencia p95 («El promedio engaña»):**
   - Demostración de `tests/smoke.py` contra Render con formato *«Una línea por caso, una línea de resultado»*: 6/6 aprobados y **p95 de 2.2 segundos**.
   - Justificación de por qué el promedio engaña: un promedio de 3.4s oculta que alguien esperó 30s; el **p95** garantiza matemáticamente que 95 de cada 100 colaboradores reciben respuesta en 2.2s o menos.

---

## 2. Banco de Preguntas Críticas de la Rúbrica Oficial (Caso 03 · Fase 5)

### Pregunta Oficial 1 (Fase 5): *«¿Qué porcentaje de solicitudes se resolvieron sin intervención humana y cómo lo demostraron?»*
* **Respuesta del Equipo:**  
  *«En nuestro conjunto oficial de evaluación de 30 solicitudes de referencia (`eval/preguntas.json`), **73.3% (22 de 30 solicitudes)** fueron resueltas exitosamente en Nivel 1 mediante autoatención RAG guiada sobre los 15 manuales técnicos internos de la PYME, superando la meta de la rúbrica ($\ge 70\%$).  
  Lo demostramos cuantitativamente: cada solicitud técnica de autoatención obtiene una cita oficial verificable (`[DOC-01 a DOC-05]`), comprueba que no existan alucinaciones y valida que el colaborador pueda resolver el incidente en su puesto sin consumir tiempo del técnico. El restante 26.7% correspondió a solicitudes con requerimiento de intervención física de hardware (rotura de cable, pantalla azul) o privilegios de administrador de dominio, las cuales fueron derivadas correctamente a Nivel 2.»*
* **Archivos de respaldo:** [`eval/run_eval.py`](eval/run_eval.py), [`eval/preguntas.json`](eval/preguntas.json) y [`app/routers/principal.py`](app/routers/principal.py) (`GET /v1/metricas/fase5`).

---

### Pregunta Oficial 2 (Fase 5): *«¿Cómo definieron y probaron la regla de escalamiento de tickets?»*
* **Respuesta del Equipo:**  
  *«La regla de escalamiento está gobernada **100% por código determinista en Python (`app/flujo.py`), nunca por la prosa del LLM**. Se definieron tres compuertas estrictas:  
  1. **Requerimiento de intervención física de hardware:** Detección de fallas no solucionables por software (rotura de cable UTP, conmutador inerte, fallo de placa base o pantalla azul BSOD recurrente).  
  2. **Umbral de Similitud Semántica RAG (< 0.85) o Consulta Fuera de Alcance:** Si el manual no cubre el problema, el sistema aplica la regla de abstención estricta, no alucina y deriva a un humano.  
  3. **Compuerta Human-in-the-Loop (HITL · OWASP LLM08):** Todo despacho técnico presencial se bloquea preventivamente (`estado: pendiente_aprobacion_humana`) hasta que un operador técnico confirme la acción.  
  Esta regla se probó exhaustivamente en `tests/test_herramientas_agente.py` (`test_tool_escalar_hitl_bloqueo_sin_confirmacion`) y en `tests/test_endpoints.py` con 100% de éxito.»*
* **Archivos de respaldo:** [`app/flujo.py`](app/flujo.py), [`app/tools/priorizar.py`](app/tools/priorizar.py) y [`tests/test_herramientas_agente.py`](tests/test_herramientas_agente.py).

---

### Pregunta Oficial 3 (Fase 5): *«¿Cuáles son las métricas de Retorno de Inversión (ROI) para la PYME de 60 colaboradores?»*
* **Respuesta del Equipo:**  
  *«Para una PYME con 60 colaboradores y un único técnico de TI desbordado, nuestro sistema de Triaje Automático de Solicitudes de Soporte Tecnológico entrega métricas de ROI medibles y contundentes:  
  1. **Reducción Drástica del MTTR (Tiempo Medio de Resolución):** Las incidencias comunes pasan de un tiempo de espera promedio de **45 minutos** a una resolución en **3.8 minutos** guiada por el paso a paso de los manuales RAG (-91.5% de tiempo de espera).  
  2. **Resolución en Primer Contacto (FCR):** Se eleva al **73.3% - 80.8%**, resolviendo incidentes al instante sin crear cuellos de botella.  
  3. **Ahorro de Tiempo del Técnico:** Al resolver el 73.3% de las solicitudes repetitivas por autoatención N1, se liberan **4.5 horas diarias** del técnico (más de **90 horas al mes**), permitiéndole enfocarse en proyectos estratégicos y ciberseguridad.  
  4. **Costo Operativo por Ticket:** El costo desciende de **$18.00 USD** (costo de atención manual personalizada) a **$3.40 USD** con autoatención inteligente (-81% de reducción).  
  5. **Ahorro Financiero Anual Proyectado:** Para un volumen estimado de 120 tickets mensuales en la PYME, el ahorro neto supera los **$16,900 USD anuales** en productividad recuperada.»*
* **Archivos de respaldo:** [`docs/01-propuesta.md`](docs/01-propuesta.md), [`config/matriz_prioridad.json`](config/matriz_prioridad.json) y el endpoint `/v1/metricas/fase5`.

---

### Pregunta Oficial 4 (Fase 5): *«¿Cómo demuestran que el sistema de Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME no está diseñado para una empresa específica, sino como una solución general para cualquier PYME?»*
* **Respuesta del Equipo:**  
  *«Demostramos la generalidad y adaptabilidad de nuestra plataforma de Triaje Automático de Solicitudes de Soporte Tecnológico a través de cuatro pilares arquitectónicos auditables:  
  1. **Universalidad de Necesidades Microinformáticas:** Los 15 manuales técnicos estándar abordan la infraestructura tecnológica que comparte cualquier PYME moderna (Active Directory / Windows / M365, clientes VPN corporativos, impresoras departamentales en red, carpetas compartidas SMB/NAS, ERPs contables y redes Wi-Fi).  
  2. **Base de Conocimiento Desacoplada y Extensible (Corpus RAG en Markdown):** El conocimiento no está quemado en el código fuente. En el propio tablero web, el botón **`📚 15 Manuales RAG`** permite al personal técnico agregar, editar o convertir documentos Word/PDF a Markdown e indexarlos en ChromaDB al instante.  
  3. **Matriz de Priorización ITIL Parametrizable:** Las reglas de negocio, niveles de severidad y tiempos máximos de SLA están desacoplados en `config/matriz_prioridad.json`. Cualquier empresa puede configurar sus propios SLAs sin alterar una sola línea de código backend.  
  4. **Esquemas Pydantic V2 Genéricos:** Los contratos procesan categorías estándar de TI de la industria, garantizando total portabilidad.»*
* **Archivos de respaldo:** [`data/raw/`](data/raw/), [`config/matriz_prioridad.json`](config/matriz_prioridad.json) y [`docs/04-fuentes.md`](docs/04-fuentes.md).

---

## 3. Banco de Preguntas Adicionales del Tribunal y Respuestas de Alto Nivel

### Pregunta 1: *«¿Por qué no le pidieron al LLM que calcule directamente la prioridad y el tiempo SLA de resolución?»*
* **Respuesta:** *«Porque los Modelos de Lenguaje son sistemas estocásticos y probabilísticos, no motores de cálculo determinista. En la gestión de servicios ITIL v4 y en acuerdos de nivel de servicio (SLA), los tiempos de respuesta tienen consecuencias contractuales y financieras que no pueden depender de la temperatura o del muestreo probabilístico de un modelo. En nuestro sistema aplicamos la regla fundacional: 'El modelo propone, el código dispone'. El LLM únicamente extrae el Impacto y la Urgencia cualitativa desde el lenguaje natural del reporte; luego, nuestra función determinista en Python lee la matriz oficial en `config/matriz_prioridad.json` y calcula la prioridad matemática y los minutos de SLA. De este modo garantizamos cero alucinaciones, 100% de reproducibilidad y cero costo de tokens.»*
* **Archivos de respaldo:** [`app/tools/priorizar.py`](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/tools/priorizar.py) y [`config/matriz_prioridad.json`](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/config/matriz_prioridad.json).

---

### Pregunta 2: *«¿Qué ocurre si durante la operación en vivo la API de Google Gemini se cae (HTTP 503) o se satura la cuota (HTTP 429)?»*
* **Respuesta:** *«Diseñamos un Gateway de Resiliencia multinivel en `ClienteLLM`. Ante un error HTTP 429, el cliente ejecuta un ciclo de hasta 3 reintentos gobernados por Exponential Backoff ($0.5s \times 2^{\text{intento}}$). Si la saturación persiste o la llamada excede el timeout estricto de 12 segundos, el sistema conmuta automáticamente en menos de 500 ms al modelo secundario Llama 3.3 70B en Groq Cloud. Si el entorno carece de conexión a internet, se activa un tercer nivel de contingencia: nuestro motor heurístico local offline. Además, cumplimos con el principio de transparencia: el payload y la interfaz web encienden un distintivo naranja informando al operador que la solicitud fue atendida por el modelo de respaldo y registrando el motivo exacto del fallo.»*
* **Archivos de respaldo:** [`app/services/llm.py`](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/services/llm.py) y [`docs/09-decisiones/ADR-003-failover-gemini-groq.md`](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/docs/09-decisiones/ADR-003-failover-gemini-groq.md).

---

### Pregunta 3: *«¿Cómo garantizan el cumplimiento de la Ley Orgánica de Protección de Datos Personales (LOPDP de Ecuador)?»*
* **Respuesta:** *«Aplicamos tres salvaguardas técnicas y legales auditables:  
  1. **Anonimización previa de credenciales (Art. 23 LOPDP):** Mediante expresiones regulares en la capa de entrada del backend, cualquier contraseña ingresada accidentalmente por el usuario es interceptada y sustituida por `[CONFIDENCIAL_REMOVIDO]` antes de enviar los datos al LLM o guardarlos en SQLite.  
  2. **Minimización de datos (Art. 10 LOPDP):** Solo se capturan los identificadores estrictamente necesarios para el triaje técnico (nombre, correo corporativo y departamento).  
  3. **Filtro de Contrato con `response_model` en FastAPI:** Evita la fuga de PII, system prompts, rutas internas o tracebacks hacia el cliente (OWASP LLM02).»*
* **Archivos de respaldo:** [`app/routers/principal.py`](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/routers/principal.py) y [`app/services/llm.py`](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/services/llm.py).

---

### Pregunta 4: *«¿Cómo mitigaron el riesgo de Inyección de Prompts y Jailbreak (OWASP LLM01)?»*
* **Respuesta:** *«Implementamos una arquitectura de Defensa en Profundidad con 4 capas:  
  1. **Aislamiento semántico XML:** La entrada del usuario nunca se concatena en prosa libre; se encapsula estrictamente dentro de etiquetas `<solicitud>{texto}</solicitud>`, instruyendo al modelo a tratarla como datos pasivos.  
  2. **Esquemas Pydantic V2 cerrados:** La configuración `model_config = ConfigDict(extra="forbid")` rechaza de inmediato cualquier payload que intente inyectar atributos espurios.  
  3. **Directiva de abstención en Prompt v3:** Instruye al modelo a rechazar instrucciones que contradigan su rol de mesa de ayuda y activar `requiere_revision_humana: true`.  
  4. **Lógica determinista:** La decisión de prioridad y escalamiento presencial la decide el código Python evaluando reglas de negocio, nunca la prosa generada por el LLM.»*
* **Archivos de respaldo:** [`app/prompts/sistema_v3.txt`](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/prompts/sistema_v3.txt) y [`docs/05-prompts.md`](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/docs/05-prompts.md).

---

### Pregunta 5: *«¿Por qué dicen que el cliente del modelo está encapsulado y cómo demuestran que cambiar de proveedor no toca los endpoints?»*
* **Respuesta:** *«Aplicamos el patrón Gateway / Strategy en `ClienteLLM`. Los controladores HTTP en FastAPI (`app/routers/principal.py`) no importan los SDKs de Google ni de Groq; únicamente consumen métodos de alto nivel: `cliente_llm.clasificar()`, `cliente_llm.chat_stream()` y `cliente_llm.analizar()`. Podemos cambiar de proveedor en tiempo de ejecución (`cliente_llm.cambiar_proveedor('groq')`) o modificando la variable `PROVEEDOR_LLM_ACTIVO` en `.env`, y los endpoints continúan recibiendo y emitiendo los mismos contratos tipados Pydantic V2 (`TicketOut`, `ResultadoAnalizarOut`). Ninguna línea de los controladores se modifica.»*
* **Archivos de respaldo:** [`app/services/llm.py`](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/services/llm.py).

---

### Pregunta 6: *«¿Cómo probaron los endpoints con `pytest` sin gastar saldo de API ni depender de conexión a internet?»*
* **Respuesta:** *«Construimos una suite de **82 pruebas unitarias automatizadas** en `tests/` utilizando dobles de prueba (`monkeypatch`). Interceptamos las funciones del cliente LLM para retornar respuestas predecibles e instantáneas que validan todo el perímetro de backend (esquemas Pydantic, cálculo ITIL, citas RAG y persistencia SQLite) en tan solo 60 segundos con $0.00 USD de gasto. Incluso implementamos la prueba `test_mock_garantia_cero_consumo_api_y_cero_red` que borra las API keys del entorno y demuestra que el sistema aprueba 100% desconectado de internet.»*
* **Archivos de respaldo:** [`tests/test_endpoints.py`](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/tests/test_endpoints.py) y [`tests/test_herramientas_agente.py`](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/tests/test_herramientas_agente.py).

---

### Pregunta 7: *«¿Cómo miden y controlan los costos de inferencia y la latencia del sistema (FinOps)?»*
* **Respuesta:** *«Implementamos un middleware de observabilidad en `app/main.py`. Por cada solicitud de inferencia se miden con `time.perf_counter()` la duración exacta en milisegundos y se contabilizan los tokens de entrada (prompt), tokens de salida (completado) y tokens totales. Estos datos se inyectan en los encabezados HTTP (`X-Response-Time-Ms`, `X-Request-ID`), se escriben en logs estructurados con formato JSON y se exponen en el endpoint de telemetría `GET /v1/metricas/solicitudes`, permitiendo a los supervisores auditar promedios, máximos y costos proyectados en tiempo real.»*
* **Archivos de respaldo:** [`app/main.py`](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/main.py).

---

### Pregunta 8: *«¿Por qué la interfaz principal es un Tablero Kanban y no un chat abierto?»*
* **Respuesta:** *«Porque en la ingeniería de soporte técnico y gestión ITIL, los incidentes no son conversaciones de ocio; son **órdenes de trabajo con estados, responsables y tiempos máximos de atención (SLA)**. Un chat abierto oculta las averías pendientes y no permite balancear la carga de trabajo del técnico de TI. El tablero Kanban permite visualizar en tiempo real qué tickets están nuevos, cuáles están en autoatención y cuáles requieren soporte presencial en el puesto de trabajo. Para asistencia interactiva complementaria, disponemos del endpoint `POST /chat` con Streaming token a token.»*
* **Archivos de respaldo:** [`frontend/index.html`](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/frontend/index.html) y [`docs/01-propuesta.md`](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/docs/01-propuesta.md).

---

### Pregunta 9: *«¿Por qué el endpoint `/health` nunca debe invocar al modelo LLM?»*
* **Respuesta:** *«Porque `/health` es una sonda de vitalidad operacional (liveness probe). Su único propósito es verificar si el servidor web, el runtime de Python y el microcontenedor están activos («estoy viva»). Si `/health` realizara una llamada a Google Gemini o Groq y la API externa sufriera latencia, timeout, cuota 429 o una caída temporal 503, la plataforma de orquestación en la nube (Render, Cloud Run, Kubernetes) asumiría erróneamente que la aplicación entera colapsó y reiniciaría en bucle el contenedor, destruyendo la disponibilidad del servicio. Además, invocar al modelo en `/health` provocaría un consumo continuo e innecesario de tokens. En nuestra arquitectura, `/health` nunca invoca al LLM y responde inmediatamente en milisegundos con `{"status": "ok"}`.»*
* **Archivos de respaldo:** [`app/routers/salud.py`](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/routers/salud.py) y [`app/main.py`](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/main.py).

---

### Pregunta 10: *«¿Dónde viven los datos en el contenedor y qué vería el usuario si desplegamos dos copias de la app, cada una con su propio SQLite?»*
* **Respuesta:** *«Bajo la premisa de que 'el contenedor nace limpio en cada arranque', clasificamos los datos en tres niveles arquitectónicos:  
  1. **Datos de solo lectura:** El índice vectorial de ChromaDB (`data/chroma/`), los 15 manuales técnicos (`data/raw/`) y la configuración ITIL (`config/`) se empaquetan dentro de la imagen Docker en el build (`COPY . .`), garantizando que la aplicación esté lista para resolver consultas desde el primer segundo.  
  2. **Datos transaccionales efímeros del MVP:** La base SQLite (`data/triaje_soporte.db`) corre en disco local con réplica única (`replicas: 1`), aceptando su reinicio limpio para garantizar costo cero y latencia menor a 1ms. Además, al arrancar, el ciclo lifespan siembra automáticamente los 20 tickets oficiales de demostración (5 por columna del Kanban) a partir de `app/datos_semilla.py`.  
  **Si desplegáramos dos copias (réplicas concurrentes) cada una con su propio SQLite:** El usuario experimentaría **inconsistencia de datos (Split-Brain / Estado Fragmentado)**. Si un colaborador crea un ticket en la Réplica A y al recargar la página el balanceador lo envía a la Réplica B, el ticket no aparecerá porque la base de B es un archivo local independiente. Por ello, la evolución a producción multi-instancia horizontal exige desacoplar SQLite hacia una base de datos externa gestionada (PostgreSQL / Supabase) o volumen persistente compartido, decisión formalmente documentada en el ADR-004.»*
* **Archivos de respaldo:** [`docs/09-decisiones/ADR-004-sqlite-persistencia-local.md`](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/docs/09-decisiones/ADR-004-sqlite-persistencia-local.md), [`Dockerfile`](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/Dockerfile) y [`app/database.py`](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/database.py).

---

## 4. Matriz de Trazabilidad: Concepto Teórico vs. Archivo en el Repositorio

| Concepto Evaluado por el Tribunal | Archivo Principal de Implementación | Justificación Técnica Breve |
|---|---|---|
| **Modelo C4 (Niveles 1 al 4)** | [docs/03-arquitectura.md](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/docs/03-arquitectura.md) | Diagramas Mermaid de Contexto, Contenedores, Componentes y Código/Secuencia. |
| **Cliente LLM Encapsulado** | [app/services/llm.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/services/llm.py) | Patrón Gateway / Strategy; conmutación en caliente sin tocar controladores. |
| **Failover Gemini $\to$ Groq** | [app/services/llm.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/services/llm.py) | Captura de errores 429/503/timeout y conmutación automática en <500 ms. |
| **Priorización Determinista ITIL** | [app/tools/priorizar.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/tools/priorizar.py) | Cálculo matemático de prioridad y SLA leyendo `config/matriz_prioridad.json`. |
| **Validación Estricta Pydantic V2** | [app/schemas.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/schemas.py) | Modelos DTO con `ConfigDict(extra="forbid")` para neutralizar OWASP LLM05. |
| **Ciberseguridad y LOPDP (Art. 23)** | [app/services/llm.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/services/llm.py) | Anonimización previa de contraseñas por Regex (`[CONFIDENCIAL_REMOVIDO]`). |
| **Limitador de Tasa Token Bucket** | [app/main.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/main.py) | 15 fichas por IP, recarga cada 3s y respuesta RFC 6585 con `Retry-After`. |
| **Observabilidad y Tokens** | [app/main.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/main.py) | Registro de tokens in/out/total, latencia y endpoint `/v1/metricas/solicitudes`. |
| **Dashboard de Métricas Fase 5** | [app/routers/principal.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/app/routers/principal.py) | Endpoint `/v1/metricas/fase5` y modal interactivo en el frontend. |
| **Pruebas con Mocks (Cero API)** | [tests/test_endpoints.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/tests/test_endpoints.py) | 82 pruebas pasando en 60s con `monkeypatch` y $0.00 USD consumidos. |
| **Auditoría Cero Secretos** | [scripts/auditar_cero_secretos.py](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/scripts/auditar_cero_secretos.py) | Verificación de exclusión de `.env` en Git e historial limpio de commits. |
| **10 Decisiones de Arquitectura** | [docs/09-decisiones/](file:///c:/Users/Cris/Downloads/Programas%20APP/Seminario/APP%20IA/docs/09-decisiones/) | Registros ADR-001 al ADR-010 con contexto, decisión y consecuencias. |

---

## 5. Protocolo de Demostración en Vivo ante el Tribunal

1. **Paso 1: Demostrar la Suite de Pruebas Offline:**
   ```powershell
   pytest -v tests/
   ```
   *Mensaje al jurado:* *"Observen cómo ejecutamos 82 pruebas unitarias automatizadas de punta a punta en segundos con cero consumo de saldo de API y garantía 100% offline."*
2. **Paso 2: Demostrar Cero Secretos y Código Seguro:**
   ```powershell
   python scripts/auditar_con_codeguard.py
   ```
   *Mensaje al jurado:* *"Auditamos la base de código contra herramientas SAST (Bandit y Ruff) confirmando 0 vulnerabilidades críticas de ciberseguridad y 0 secretos expuestos en Git."*
3. **Paso 3: Triaje en Vivo en el Frontend (`https://triajesoporte-grupo-3.onrender.com/tablero`):**
   - Hacer clic en el botón de ejemplo rápido: **`🔑 Clave AD Bloqueada (DOC-01)`**.
   - Presionar **`⚡ Clasificar con IA y Crear Ticket`**.
   - Mostrar el spinner reactivo mientras la IA procesa.
   - Mostrar el ticket generado en la columna **`Nuevos`** con Prioridad Baja, SLA de 1440m y la cita técnica obligatoria del manual oficial **`[DOC-01 · Paso 2]`**.
4. **Paso 4: Demostración del Dashboard de Métricas y ROI (Fase 5):**
   - Activar el botón **`👨‍💻 Vista TIC`** en la barra superior.
   - Hacer clic en **`📊 Métricas y ROI (Fase 5)`**.
   - Mostrar al docente la tasa de autoatención (73.3%), las 3 compuertas de la regla de escalamiento y el retorno financiero anual (\$16,987 USD/año).
5. **Paso 5: Demostración del Modo Vulnerable (Chaos Engineering):**
   - En la Barra Chaos, desactivar **"Defensas IA"** y presionar **`🌀 Inyección Prompt & Failover`**.
   - Mostrar cómo el modelo desprotegido alucina Prioridad Alta y el documento inexistente DOC-99.
   - Reactivar **"Defensas IA"** y repetir la prueba: el sistema neutraliza el intento dentro de `<solicitud>`, responde con Prioridad Baja determinista y preserva la integridad del servicio.
