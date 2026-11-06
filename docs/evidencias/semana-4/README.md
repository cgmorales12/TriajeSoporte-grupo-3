# Evidencias de Trabajo y Práctica: Semana 4 · Versión Final Desplegada y Certificación QA

**Proyecto:** Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME  
**Caso Asignado:** Caso N.º 03 (Mesa de Ayuda y Soporte Microinformático TIC para PYME de 60 Colaboradores)  
**Seminario de Titulación:** Ingeniería de Software con IA Generativa — UNIANDES (Octubre – Noviembre 2026)  
**Integrantes del Grupo 3:**  
1. **Christian Guillermo Morales González** (Tech Lead / Coordinador — GitHub: `cgmorales12`)  
2. **Luis Fernando Ribera Alajo** (Builder / Arquitectura — GitHub: `fernandolribera`)  
3. **Amalia Geoconda Iguasnia Escobar** (QA Lead / Seguridad y Requerimientos — GitHub: `Geocoiguasnia76`)  
**Docente Evaluador:** Heyler Fabio Guaza (Ing. Informático · Mg. en Ciberseguridad · OPD · Abogado)  
**Periodo de Evaluación:** Semana 4 — Versión Final Desplegada, Evaluación Rigurosa (Hit@5, Alucinación Cero, Determinismo) y Auditoría LOPDP / OWASP  
**Repositorio GitHub:** `https://github.com/cgmorales12/TriajeSoporte-grupo-3`  

---

## 1. Resumen Ejecutivo del Cierre de Semana 4

Durante la Semana 4 se consolidó la **versión final del MVP**, certificando todos los requerimientos funcionales y no funcionales del sistema bajo el principio rector:
> ***«El modelo propone, el código dispone, la configuración gobierna, el humano autoriza.»***

El control de calidad (QA) y auditoría de ciberseguridad liderado por Amalia Iguasnia verificó:
1. **100% de Pruebas Automatizadas Exitosas:** 82 casos de prueba unitarios e integración en `tests/` ejecutados sin fallos con mocks deterministas (sin consumo innecesario de tokens ni caídas por conectividad).
2. **Métricas de Evaluación IA Óptimas:**
   - **RAG Hit@5:** $\ge 92.9\%$ de recuperación relevante sobre los 15 manuales PYME oficiales.
   - **Tasa de Alucinación:** $0.0\%$ (mitigada por abstención activa y contratos Pydantic con `extra="forbid"`).
   - **Determinismo ITIL:** $100.0\%$ de consistencia en el cálculo matemático de prioridad y SLA desde `config/matriz_prioridad.json`.
3. **Auditoría de Ciberseguridad y Privacidad LOPDP:**
   - Cero secretos expuestos en Git (`.env` verificado en `.gitignore` y auditado con script SAST).
   - Anonimización preventiva de credenciales (expresiones regulares sustituyen contraseñas por `[CONFIDENCIAL_REMOVIDO]`).
   - Mitigación de Exceso de Agencia (OWASP LLM08) mediante Confirmación Humana Obligatoria (HITL) previa a la persistencia.

---

## 2. Matriz de Cumplimiento de la Lista de Verificación (Entrega 4)

| Requisito de la Plataforma | Estado | Evidencia y Justificación Técnica |
| :--- | :---: | :--- |
| **Grupo y Proyecto Declarado** | ✅ CUMPLIDO | Grupo 3 · Caso N.º 03 (`Triaje Soporte`) |
| **Integrantes Registrados** | ✅ CUMPLIDO | AMALIA IGUASNIA // LUIS RIBERA // CHRISTIAN MORALES |
| **Repositorio GitHub Oficial** | ✅ CUMPLIDO | `https://github.com/cgmorales12/TriajeSoporte-grupo-3` |
| **URL Pública con `/health`** | ✅ CUMPLIDO | Endpoint `/health` responde `{"status": "ok", ...}` conforme al RFC 9457 |
| **RAG sobre 15 Manuales Oficiales** | ✅ CUMPLIDO | ChromaDB con 90 fragmentos estructurados con metadatos de vigencia |
| **HITL (Confirmación Humana)** | ✅ CUMPLIDO | Interfaz modal interactiva que previene el registro sin validación humana |
| **Manejo de Errores RFC 9457** | ✅ CUMPLIDO | Payloads estructurados con `type`, `title`, `status`, `detail` e `instance` |
| **Cero Secretos en Repositorio** | ✅ CUMPLIDO | Certificación emitida por `scripts/auditar_cero_secretos.py` |

---

## 3. Certificación de Calidad y Pruebas Unitarias

```text
============================= test session starts =============================
platform win32 -- Python 3.11.x, pytest-8.3.3
collected 82 items

tests/test_endpoints.py ................................................ [ 58%]
tests/test_endpoints.py ..................................               [100%]

======================== 82 passed, 1 warning in 51.67s ========================
```

---

*Documento certificado por el área de QA y Requerimientos — Grupo 3 UNIANDES.*
