# Declaración Formal de Uso de Inteligencia Artificial y Tabla de Aportes por Integrante

**Proyecto:** Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME  
**Caso Asignado:** Caso N.º 03 (Mesa de Ayuda y Soporte Microinformático TIC para PYME de 60 Colaboradores)  
**Seminario de Titulación:** Ingeniería de Software con IA Generativa — UNIANDES (Octubre – Noviembre 2026)  
**Docente Evaluador:** Heyler Fabio Guaza (Ing. Informático · Mg. en Ciberseguridad · OPD · Abogado)  
**Repositorio GitHub Oficial:** [https://github.com/cgmorales12/TriajeSoporte-grupo-3](https://github.com/cgmorales12/TriajeSoporte-grupo-3)  
**URL Pública Desplegada:** [https://triajesoporte-grupo-3.onrender.com](https://triajesoporte-grupo-3.onrender.com)  

---

## 1. Declaración Formal sobre el Uso Ético de Inteligencia Artificial

Los suscritos estudiantes del Grupo 3 declaramos de manera expresa, transparente y formal:

1. **Uso de IA en el Producto (Runtime):**
   - El sistema integra modelos de Inteligencia Artificial Generativa (**Google Gemini 1.5 Flash / 3.5 Flash Lite** como motor primario y **Llama 3.3 70B en Groq Cloud** como respaldo de contingencia) exclusivamente para la extracción de síntomas, clasificación inicial y redacción amigable de autoatención.
   - Todo el comportamiento del modelo está gobernado bajo el principio rector:
     > ***«El modelo propone, el código dispone, la configuración gobierna, el humano autoriza.»***
   - El LLM tiene terminantemente prohibido calcular prioridades ITIL, estimar minutos de SLA, fijar presupuestos o despachar técnicos sin confirmación humana previa (HITL - OWASP LLM08).

2. **Uso de IA en el Proceso de Desarrollo (Asistencia Tecnológica y Transparencia):**
   - En concordancia con las directrices del *Seminario de Titulación en Ingeniería de Software con IA Generativa*, se emplearon herramientas de IA generativa de manera ética y transparente como soporte para la estructuración de escenarios de prueba, optimización sintáctica y diseño conceptual.
   - **Autoría, Control y Responsabilidad Humana:** Todo el código fuente, la lógica determinista de la matriz ITIL v4, los esquemas Pydantic V2 cerrados, la integración con ChromaDB, el repositorio SQLite y la suite de pruebas unitarias fueron conceptualizados, programados, auditados, comprendidos y validados directamente por los integrantes del equipo.

3. **Protección de Datos y Confidencialidad:**
   - No se utilizaron datos reales de clientes ni colaboradores.
   - El sistema aplica anonimización activa de credenciales (LOPDP Art. 23) y opera bajo directivas de cero retención de datos para entrenamiento.

---

## 2. Tabla Oficial de Aportes y Responsabilidades por Integrante

| Integrante | Rol en el Proyecto | Usuario GitHub | Horas Aprox. | Aportes Técnicos Principales y Módulos Desarrollados |
| :--- | :--- | :---: | :---: | :--- |
| **Christian Guillermo Morales González** | Tech Lead / Coordinador | [`cgmorales12`](https://github.com/cgmorales12) | ~45h | • Diseño y desarrollo de la arquitectura REST en FastAPI con AnyIO.<br>• Gateway de resiliencia con conmutación transparente Gemini -> Groq -> Local.<br>• Despliegue en la nube en Render Cloud (Docker multi-stage) y healthcheck `/health`.<br>• Coordinación general, unificación del README y observabilidad de tokens. |
| **Luis Fernando Ribera Alajo** | Builder / Arquitectura | [`fernandolribera`](https://github.com/fernandolribera) | ~40h | • Matriz ITIL v4 determinista (`config/matriz_prioridad.json` y `app/tools/priorizar.py`).<br>• Repositorio SQLite parametrizado contra inyecciones SQL.<br>• Motor RAG en ChromaDB persistente y chunking jerárquico de los 15 manuales PYME.<br>• Desacoplamiento de tarifas, SBU $482 y calendario de feriados en `config/`. |
| **Amalia Geoconda Iguasnia Escobar** | QA Lead / Seguridad | [`Geocoiguasnia76`](https://github.com/Geocoiguasnia76) | ~42h | • Validación de contratos con Pydantic V2 (`extra="forbid"`).<br>• Perímetro de ciberseguridad OWASP LLM 2025 y cumplimiento LOPDP Art. 23.<br>• Suite de 82 pruebas automatizadas con Mocks deterministas (`tests/`).<br>• Batería de 16 pruebas en producción contra Render (`docs/08-pruebas.md`).<br>• Auditoría de cero secretos en Git y control de calidad. |

---

*Declaración suscrita por el equipo del Grupo 3 — UNIANDES 2026.*

