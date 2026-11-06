# Ingeniería de Requisitos: ConectaTec (Mesa de Ayuda PYME)

## 1. Introducción
El presente documento describe los requisitos funcionales y no funcionales de **ConectaTec** (Caso N.º 03 · Grupo 3 UNIANDES), sistema de triaje automático de incidentes de soporte tecnológico para Pequeñas y Medianas Empresas (PYMEs).
Las historias de usuario siguen el estándar **INVEST** y sus criterios de aceptación están redactados bajo la sintaxis **Gherkin (Dado... Cuando... Entonces...)**.

---

## 2. Historias de Usuario (8 Requisitos Funcionales Esenciales)

### HU-01: Desbloqueo y Restablecimiento de Credenciales de Red (Active Directory)
* **Como** colaborador de la PYME,
* **quiero** solicitar asistencia cuando mi cuenta corporativa se bloquee por intentos fallidos,
* **para** reanudar mis labores de oficina sin esperar horas la intervención manual del técnico.
* **Criterios de Aceptación (Gherkin):**
  * *Escenario 1: Detección y guía de auto-restablecimiento.*
    * **Dado** que el colaborador describe "cuenta bloqueada" u "olvidé mi clave de Windows",
    * **cuando** el sistema realiza el triaje semántico,
    * **entonces** clasifica la solicitud en "Accesos y Contraseñas", cita el procedimiento oficial DOC-01 e indica los pasos para desbloqueo seguro.
  * *Escenario 2: Protección LOPDP de contraseñas accidentales.*
    * **Dado** que el usuario escribe su contraseña accidentalmente en el formulario,
    * **cuando** el backend recibe el payload,
    * **entonces** la anonimiza inmediatamente como `[CONFIDENCIAL_REMOVIDO]` antes de persistir o enviar al LLM.

---

### HU-02: Diagnóstico y Configuración de VPN Corporativa para Teletrabajo
* **Como** empleado en modalidad de teletrabajo,
* **quiero** diagnosticar fallas de conexión en mi cliente FortiClient / OpenVPN,
* **para** conectarme de forma segura a los servidores internos de la empresa.
* **Criterios de Aceptación (Gherkin):**
  * *Escenario 1: Error de túnel remoto.*
    * **Dado** que el usuario reporta "error en VPN" o "FortiClient se queda en 48%",
    * **cuando** el sistema consulta la base RAG,
    * **entonces** retorna las instrucciones del manual DOC-02 verificando el gateway `vpn.empresa.com`, puerto SSL 443 y token 2FA.

---

### HU-03: Solución de Problemas en Impresoras Departamentales de Red
* **Como** colaborador de oficina,
* **quiero** resolver incidencias de atasco de papel o fallas en la cola de impresión,
* **para** imprimir documentos urgentes sin detener los procesos del área.
* **Criterios de Aceptación (Gherkin):**
  * *Escenario 1: Atasco o error de spooler.*
    * **Dado** que se reporta "atasco de papel en bandeja" o "la impresora no imprime",
    * **cuando** el motor RAG evalúa la solicitud,
    * **entonces** recupera el procedimiento DOC-03 con los pasos para despejar el recorrido de papel y reiniciar el spooler local.

---

### HU-04: Mapeo y Acceso a Carpetas Compartidas en Red (SMB / NAS)
* **Como** miembro de un departamento (Finanzas, Ventas, Operaciones),
* **quiero** restaurar mi acceso a la unidad compartida de red (Unidad Z:),
* **para** acceder a los archivos de trabajo corporativos.
* **Criterios de Aceptación (Gherkin):**
  * *Escenario 1: Acceso denegado en unidad de red.*
    * **Dado** que el colaborador indica "error de red en carpeta compartida",
    * **cuando** el sistema procesa el incidente,
    * **entonces** provee el procedimiento DOC-04 indicando la reconexión mediante comando `net use` y validación de permisos.

---

### HU-05: Desbloqueo de Sesiones en Sistema Contable / ERP Interno
* **Como** usuario del sistema contable,
* **quiero** liberar mi usuario cuando el sistema reporte una sesión concurrente colgada,
* **para** continuar con la emisión de facturas electrónicas sin duplicar registros.
* **Criterios de Aceptación (Gherkin):**
  * *Escenario 1: Sesión colgada en ERP.*
    * **Dado** que el usuario reporta "usuario ya tiene una sesión activa en ERP",
    * **cuando** el sistema clasifica la incidencia,
    * **entonces** asigna Prioridad Alta según la matriz ITIL y deriva la solicitud a Nivel 2 para liberación de sesión en la base de datos transaccional.

---

### HU-06: Escalamiento Presencial ante Fallas Críticas de Hardware (BSOD / Disco)
* **Como** técnico único de TI,
* **quiero** que las averías físicas no solucionables por software se escalen de inmediato con alerta,
* **para** acudir presencialmente al puesto de trabajo del colaborador con los repuestos adecuados.
* **Criterios de Aceptación (Gherkin):**
  * *Escenario 1: Detección de fallo de hardware.*
    * **Dado** que el reporte describe "pantalla azul BSOD", "ruido metálico de disco" o "humo",
    * **cuando** el sistema evalúa la solicitud,
    * **entonces** activa la bandera `requiere_visita_campo=True`, asigna Prioridad Alta (SLA 15m) y notifica al técnico para atención en sitio.

---

### HU-07: Priorización Determinista ITIL v4 (Cálculo sin Tokens)
* **Como** responsable de soporte,
* **quiero** que el cálculo de prioridad y tiempo SLA se gobierne por código determinista leyendo un archivo JSON,
* **para** garantizar tiempos contractuales exactos sin depender de la temperatura del LLM.
* **Criterios de Aceptación (Gherkin):**
  * *Escenario 1: Matriz determinista.*
    * **Dado** cualquier incidente con Impacto y Urgencia extraídos por IA,
    * **cuando** el backend calcula la prioridad,
    * **entonces** una función pura en Python consulta `config/matriz_prioridad.json` con 0 gasto de tokens.

---

### HU-08: Gestión Visual en Tablero Kanban con Compuertas HITL
* **Como** técnico de TI y supervisor,
* **quiero** gestionar las solicitudes en un tablero Kanban con estados (`Nuevo`, `En Atención`, `Escalado N2`, `Resuelto N1`),
* **para** supervisar la carga de trabajo y autorizar acciones de alto riesgo con confirmación humana.
* **Criterios de Aceptación (Gherkin):**
  * *Escenario 1: Compuerta Human-in-the-Loop.*
    * **Dado** un ticket que requiere derivación presencial,
    * **cuando** el agente propone la acción,
    * **entonces** exige confirmación explícita del operador antes de emitir la orden formal.
