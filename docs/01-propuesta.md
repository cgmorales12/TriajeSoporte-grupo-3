# Propuesta del Proyecto: Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME

## 1. Identificación del Proyecto
* **Producto:** **Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME** (Sistema Genérico y Configurable de Soporte Microinformático TIC)
* **Caso Asignado Oficial:** **Caso N.º 03 (Grupo 3)** — *Triaje automático de solicitudes de soporte tecnológico para una PYME (Clasificación y resolución de tickets con RAG sobre manuales internos – Agente de gestión de incidentes)*
* **Institución:** Universidad Regional Autónoma de Los Andes (UNIANDES)
* **Carrera:** Software — Seminario de Titulación Complexivo en IA Generativa (2026)
* **Integrantes del Grupo 3:**
  * **Christian Guillermo Morales González** (Tech Lead / Coordinador — `cgmorales12`)
  * **Luis Fernando Ribera Alajo** (Builder / Arquitectura — `fernandolribera`)
  * **Amalia Geoconda Iguasnia Escobar** (QA / Seguridad y Requerimientos — `Geocoiguasnia76`)

---

## 2. Definición del Problema Real (Ámbito PYME General)
En el sector empresarial, las **Pequeñas y Medianas Empresas (PYMEs)** —ya sean de servicios profesionales, comercio, logística, consultoría o manufactura ligera— comparten una problemática operativa común:
1. Cuentan con un equipo de soporte tecnológico sumamente reducido (típicamente **un único técnico o responsable de TI**) para atender a una plantilla de entre **50 y 100 colaboradores**.
2. Más del **70% de las solicitudes diarias son repetitivas** y corresponden a ofimática y servicios básicos:
   - Restablecimiento y desbloqueo de contraseñas de red (Active Directory / Windows / Correo).
   - Configuración de clientes VPN corporativos para teletrabajo.
   - Atascos de papel, colas de impresión y configuración de impresoras de red departamentales.
   - Acceso denegado y mapeo de unidades en carpetas compartidas (SMB / NAS).
   - Bloqueos de sesión concurrente en el sistema contable / ERP institucional.
   - Conexión al Wi-Fi corporativo seguro y red cableada de oficina.
3. Este volumen desborda al técnico, quien pierde entre **15 y 20 horas semanales** en tareas mecánicas, disparando el tiempo medio de resolución (**MTTR** inicial de 4 horas) y retrasando la atención de incidentes críticos de infraestructura o ciberseguridad.

---

## 3. Filosofía del Sistema: Diseñado para Cualquier PYME
**TecnoAula NO está acoplado a una empresa específica**, sino concebido como un **sistema estándar, desacoplado y parametrizable** para cualquier organización:
- **Base de Conocimiento Universal:** El corpus de 15 manuales técnicos estándar cubre las necesidades tecnológicas transversales de cualquier oficina moderna bajo normas internacionales (ISO/IEC 27002, IEEE 802.3, Wi-Fi Alliance).
- **Matriz ITIL Desacoplada (`config/matriz_prioridad.json`):** Cualquier PYME puede ajustar sus tiempos SLA contractuales y niveles de impacto/urgencia sin tocar una sola línea de código backend.
- **Configuración Paramétrica (`config/parametros.yaml`):** Umbrales de confianza, límites de iteraciones y políticas operativas se adaptan por archivo externo.
- **Corpus Extensible:** La empresa simplemente añade o modifica sus manuales en formato Markdown en `data/raw/` y re-ejecuta `python scripts/ingest.py`.

---

## 4. Usuarios del Sistema
1. **Colaborador / Empleado de la PYME:** Reporta incidencias mediante un formulario web intuitivo y recibe instrucciones paso a paso con citas exactas para resolver su problema de forma autónoma (Nivel 1).
2. **Técnico de TI / Administrador de Soporte:** Monitorea y gestiona las solicitudes a través de un **Tablero Kanban de Tickets con 4 estados** (`Nuevo`, `En Atención`, `Escalado a Técnico N2`, `Resuelto N1`).
3. **Supervisor / Gerencia:** Audita métricas de servicio (MTTR, % de autoatención $\ge 70\%$, tokens consumidos y ROI generado).

---

## 5. Alcance del Sistema

### 5.1 Alcance Positivo (Capacidades del Sistema)
* **Clasificación Estructurada (IA):** Extracción precisa de categoría técnica, impacto y urgencia mediante JSON estricto validado con Pydantic V2 (`extra="forbid"`).
* **Priorización Determinista (Código Python Puro):** Cálculo matemático de la prioridad (`Alta`, `Media`, `Baja`) y SLA en minutos leyendo `config/matriz_prioridad.json`. *«El modelo propone, el código dispone»*.
* **Resolución de Nivel 1 con RAG:** Búsqueda semántica en ChromaDB sobre los 15 manuales técnicos citando documento y paso exacto.
* **Escalamiento Controlado a Nivel 2:** Derivación presencial obligatoria ante fallas de hardware (ruido metálico de disco, pantalla azul BSOD, daño de cableado) o requerimiento de credenciales administrativas.
* **Compuertas Human-in-the-Loop (HITL · OWASP LLM08):** Todo despacho físico o notificación formal exige confirmación explícita de un operador humano.
* **Resiliencia y Failover:** Conmutación automática ante errores HTTP 429/503 desde Gemini 1.5 Flash hacia Groq Cloud (Llama 3.3 70B) y motor heurístico local offline.

### 5.2 Alcance Negativo (Límites Inviolables)
* **Cero Contraseñas Almacenadas (Art. 23 LOPDP):** El sistema detecta por Regex y anonimiza con `[CONFIDENCIAL_REMOVIDO]` cualquier credencial escrita por error.
* **Cero Alucinaciones Fuera de Alcance:** Ante consultas no técnicas o ajenas a la infraestructura TI, el sistema aplica la regla de silencio y orienta al colaborador.
* **El LLM jamás calcula prioridades:** Ni inventa tiempos de SLA ni modifica la base de datos de tickets de forma autónoma.

---

## 6. Métricas de Retorno de Inversión (ROI) para la PYME
1. **Autoatención Nivel 1 $\ge 70\%$:** Más de 7 de cada 10 solicitudes resueltas sin intervención humana.
2. **Ahorro de ~15 horas semanales** para el técnico de TI (más de 60 horas al mes liberadas).
3. **Reducción del MTTR de 4 horas a menos de 2 minutos** para incidencias de primer nivel.
4. **Costo evitado de contratación** de un segundo técnico ($800 a $1.000 USD mensuales).
5. **Costo de inferencia menor a $0.002 USD por ticket**, con gasto mensual de IA inferior a $1.50 USD.
