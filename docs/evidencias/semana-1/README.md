# Evidencias de Trabajo y Práctica: Semana 1 - Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME

## 1. Identificación del Equipo y Proyecto
* **Proyecto:** Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME - Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME (Caso N.º 03 · Grupo 3)
* **Caso Asignado:** Caso N.º 03 (Grupo 3)
* **Integrantes:**
  * Christian Guillermo Morales González
  * Luis Fernando Ribera Alajo
  * Amalia Geoconda Iguasnia Escobar
* **Periodo de Evaluación:** Semana 1 - Arquitectura, Fundamentos de LLM y Requisitos

---

## 2. Decisiones Técnicas Clave de la Semana 1
1. **Modelo Generativo Principal:** Se seleccionó `gemini-1.5-flash` por su latencia reducida (< 3 s), soporte nativo para esquemas JSON estructurados y capa gratuita operativa.
2. **Estrategia de Tolerancia a Fallos:** Conmutación automática (*fallback*) hacia `Groq` con `llama-3.3-70b-versatile` ante errores de cuota o rate limit (`HTTP 429`).
3. **Determinismo en Priorización:** El cálculo de la prioridad (Crítica, Alta, Media, Baja) se implementa mediante código Python estricto aplicando la matriz ITIL versionada, delegando al LLM únicamente la extracción de impacto y urgencia.
4. **Cumplimiento de Privacidad (LOPDP):** Se implementó una directiva estricta de sanitización de credenciales y contraseñas de red antes del procesamiento en backend.

---

## 3. Práctica de Evaluación de Respuestas del Modelo (Clase 1)
Evaluación de 3 consultas técnicas de soporte microinformático realizadas contra `gemini-1.5-flash` para medir precisión técnica y alucinaciones:

| N.º | Consulta Enviada al LLM | Respuesta Obtenida del Modelo | Evaluación | Justificación Técnica |
| :---: | :--- | :--- | :---: | :--- |
| **01** | *"¿Por qué mi cuenta de Windows en Active Directory aparece bloqueada tras ingresar 3 veces mal la contraseña y qué debo hacer?"* | Explicó que indica una política de bloqueo por umbral de intentos fallidos y sugirió esperar 15 minutos o contactar al administrador para desbloqueo mediante consola. | **Correcta** | Coincide 100% con el procedimiento oficial `DOC-01` de Active Directory para restablecimiento seguro de credenciales. |
| **02** | *"Estoy en teletrabajo y el cliente VPN FortiClient se detiene en 48% con error de túnel. ¿El servidor de la empresa se cayó?"* | Afirmó categóricamente que el servidor corporativo estaba caído sin consultar el estado del gateway ni la autenticación de doble factor. | **Incorrecta** | Ignoró el fallo típico de negociación TLS/puerto 443 y el vencimiento del token 2FA (`DOC-02`). El procedimiento oficial exige validar conectividad hacia `vpn.empresa.com`. |
| **03** | *"¿La política de contraseñas de la empresa permite reutilizar las últimas 3 claves modificando solo un número?"* | Indicó que dependía de la configuración de historial de contraseñas configurada en la directiva de grupo del dominio. | **No verificable** | Depende de la directiva de grupo GPO específica del controlador de dominio y la política ISO/IEC 27002 (`DOC-06`), requiriendo verificación en la consola de administración. |

---

## 4. Registro de Colaboración Git (Semana 1)
* **Christian Morales:** Definición de propuesta de proyecto (`docs/01-propuesta.md`), inventario de fuentes técnicas (`docs/04-fuentes.md`) y consolidado de evidencias (`docs/evidencias/semana-1/README.md`).
* **Amalia Iguasnia:** Especificación de historias de usuario con criterios Gherkin y RNF (`docs/02-requisitos.md`) y levantamiento de preguntas frecuentes (`docs/05-preguntas-frecuentes.md`).
* **Luis Fernando Ribera:** Arquitectura del sistema C4 Nivel 1 y 2, endpoints FastAPI y secuencia de triaje (`docs/03-arquitectura.md`), junto con la base técnica en `data/raw/README.md`.
