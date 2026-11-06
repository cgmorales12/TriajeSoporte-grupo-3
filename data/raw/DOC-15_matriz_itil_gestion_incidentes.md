# DOC-15: Procedimiento Operativo Estándar ITIL 4 para Triaje, Priorización y Escalamiento

**Categoría:** Gestión de Incidentes ITIL  
**Origen:** Departamento de TI — InnovaServicios PYME  
**Vigencia:** 2026 (Marco de Gestión de Servicios de TI - ITIL v4)  
**URL:** https://soporte.pyme-innovaservicios.com/manuales/DOC-15_matriz_itil_gestion_incidentes.md

## Descripción General
Protocolo estándar de la empresa para la clasificación, priorización determinista y reglas de escalamiento de tickets de soporte tecnológico para los 60 colaboradores de InnovaServicios.

## Procedimiento Operativo Paso a Paso

### Paso 1: Clasificación de Incidentes por Impacto y Urgencia
Cada solicitud recibida se clasifica evaluando dos dimensiones objetivas:
- **Impacto:**
  * **Alto:** Afecta a un departamento completo, al servidor central de archivos, al sistema contable o a la salida general a internet.
  * **Medio:** Afecta a un grupo de 2 a 5 colaboradores o degrada una función de trabajo no crítica.
  * **Bajo:** Afecta a un solo colaborador en una tarea individual que dispone de alternativas temporales.
- **Urgencia:**
  * **Alta:** La tarea afectada tiene plazo de entrega inmediato (vencimiento de impuestos, cierre de facturación).
  * **Media:** Dificulta el trabajo del día pero permite avanzar en otras actividades laborales.
  * **Baja:** Consulta informativa, mantenimiento preventivo o solicitud de configuración planificada.

### Paso 2: Cálculo Determinista de Prioridad y SLA (Matriz ITIL)
La prioridad NUNCA es calculada al azar por el modelo generativo; se obtiene leyendo la matriz determinista JSON:
- Impacto Alto x Urgencia Alta = **Prioridad Alta** (SLA: 15 a 30 minutos).
- Impacto Alto x Urgencia Media / Impacto Medio x Urgencia Alta = **Prioridad Alta** (SLA: 60 minutos).
- Impacto Medio x Urgencia Media / Impacto Bajo x Urgencia Alta = **Prioridad Media** (SLA: 4 horas laborables).
- Impacto Bajo x Urgencia Media / Impacto Bajo x Urgencia Baja = **Prioridad Baja** (SLA: 8 a 24 horas laborables).

### Paso 3: Triaje de Primer Nivel (N1) y Autoatención Guiada
1. El motor de triaje busca en la base vectorial los manuales oficiales de la empresa (DOC-01 al DOC-14).
2. Si existe un procedimiento probado, responde al colaborador con el paso a paso exacto citando el documento y sección.
3. Se estima que al menos el **70%** de las consultas repetitivas (desbloqueo de contraseñas, VPN, atascos de cola de impresión) se resuelven satisfactoriamente en este nivel sin requerir la intervención del técnico de TI.

### Paso 4: Reglas de Escalamiento a Segundo Nivel (N2 - Técnico de TI)
El sistema escala el incidente creando un ticket formal en el tablero Kanban en los siguientes casos:
1. **Requerimiento de Privilegios de Administrador:** Cuando el manual estipula que la acción requiere acceso a la consola de Active Directory o al servidor central.
2. **Falla Física / Hardware:** Atascos mecánicos de impresoras, rotura de cables, daños de disco o pantallas defectuosas.
3. **No Resolución en Primer Nivel:** Si el colaborador aplica los pasos del manual y declara que el problema persiste.
4. **Validación Humana (HITL):** El técnico de TI revisa y confirma el escalamiento antes de comprometer el tiempo de SLA.
