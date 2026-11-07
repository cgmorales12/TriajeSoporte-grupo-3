# Manual de Usuario · Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME
**Sistema de Triaje Inteligente y Mesa de Ayuda para Soporte Microinformático (Caso N.º 03 · Grupo 3 UNIANDES)**

---

## 1. Introducción
La plataforma de **Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME** es una mesa de ayuda tecnológica basada en un **Tablero Kanban de Tickets** diseñada para automatizar la recepción, diagnóstico de primer nivel (RAG) y priorización determinista de incidencias para cualquier Pequeña o Mediana Empresa (PYME).

---

## 2. Acceso a la Plataforma Web
1. Abra su navegador web (Google Chrome, Firefox o Microsoft Edge).
2. Ingrese a la dirección del sistema:
   - **Local:** [http://localhost:8000/tablero](http://localhost:8000/tablero) o [http://localhost:8501](http://localhost:8501)
   - **Producción en la Nube (Render):** [https://triajesoporte-grupo-3.onrender.com/tablero](https://triajesoporte-grupo-3.onrender.com/tablero)
3. En la parte superior observará el distintivo en tiempo real del motor de IA:
   - `[Nominal] Proveedor: Gemini 1.5 Flash (Nominal)`: Operación estándar de alta velocidad.
   - `[Respaldo] Respaldo Activo: Groq Cloud (Llama 3.3)`: Conmutación automática por contingencia.

---

## 3. Ingreso de una Solicitud de Soporte (Colaborador / Empleado)

En el panel lateral izquierdo encontrará el formulario de ingreso:

```
┌──────────────────────────────────────────────┐
│       INGRESAR SOLICITUD DE SOPORTE          │
├──────────────────────────────────────────────┤
│ Nombre del Colaborador: [ Carlos Mendoza   ] │
│ Correo / Departamento:  [ carlos@empresa.com]│
│ ID de Equipo / Puesto:  [ PC-FIN-04        ] │
│ Descripción:                                 │
│ [ Olvidé mi contraseña de Windows y mi     ] │
│ [ cuenta de Active Directory se bloqueó.   ] │
├──────────────────────────────────────────────┤
│ [  Clasificar con IA y Crear Ticket ]       │
└──────────────────────────────────────────────┘
```

### Pasos:
1. Complete los campos obligatorios: Nombre, Correo y Descripción del problema (mínimo 10 caracteres).
2. O seleccione un escenario rápido de prueba (Desbloqueo de clave, Error en VPN, Atasco de impresora, Sesión ERP).
3. Haga clic en **« Clasificar con IA y Crear Ticket»**.
4. El sistema en menos de 1 segundo:
   - Sanitiza automáticamente contraseñas si las escribió por error (cumplimiento LOPDP).
   - Extrae la categoría técnica, impacto y urgencia con IA.
   - Calcula la Prioridad ITIL y el SLA mediante código determinista en Python.
   - Consulta los 15 manuales técnicos en ChromaDB y muestra la solución guiada con cita exacta.

---

## 4. Gestión de Tickets en el Tablero Kanban (Técnico de TI)
El tablero Kanban organiza las incidencias en **4 columnas operativas**:
1. **[Nuevo] Nuevos:** Solicitudes recién ingresadas pendientes de atención.
2. ** En Atención:** Incidentes en proceso de diagnóstico o resolución.
3. ** Escalados (Nivel 2):** Casos que requieren atención presencial del técnico de TI en el puesto del usuario o permisos administrativos de servidor.
4. **[OK] Resueltos (Nivel 1):** Incidentes solucionados mediante autoatención guiada con citas del manual técnico.

### Acciones Human-in-the-Loop (HITL):
- ** Notificar:** Envía formalmente la resolución al colaborador previa aprobación del técnico.
- ** Derivar a Técnico:** Genera la orden de intervención presencial con firma del responsable de soporte.
