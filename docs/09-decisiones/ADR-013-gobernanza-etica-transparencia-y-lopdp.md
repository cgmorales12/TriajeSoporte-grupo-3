# ADR-013: Gobernanza Ética, Transparencia de IA y Protección de Datos Personales (LOPDP Ecuador)
**Estado:** Aceptado  
**Fecha:** Noviembre 2026  
**Autores:** Christian Morales, Luis Fernando Ribera, Amalia Geoconda Iguasnia  
**Docente Evaluador:** Heyler Fabio Guaza (Ing. Informático · Mg. en Ciberseguridad · OPD · Abogado)  
**Proyecto:** Triaje Automático de Solicitudes de Soporte Tecnológico para una PYME (Caso N.º 03 · Grupo 3 UNIANDES)  

---

## 1. Contexto y Problema
El uso de sistemas de Inteligencia Artificial Generativa en el soporte tecnológico corporativo plantea desafíos éticos y legales críticos:
1. **Transparencia y Explicabilidad (XAI):** Los colaboradores que reportan un fallo tecnológico tienen derecho a conocer si su solicitud está siendo procesada o asistida por un modelo de Inteligencia Artificial y bajo qué criterios se clasifica su incidente.
2. **Protección de Datos Personales (LOPDP Ecuador):** La Ley Orgánica de Protección de Datos Personales exige el principio de minimización (Art. 10), recolectando únicamente los datos estrictamente necesarios para la finalidad de soporte, y la seguridad en el tratamiento de credenciales (Art. 23).
3. **Límites de la IA:** Un modelo generativo no debe sustituir el juicio humano en decisiones que afecten contratos de servicio (SLAs), ni pretender resolver fallos físicos de infraestructura sin derivación a soporte presencial.

---

## 2. Decisión de Arquitectura y Principios Éticos
Se adopta una gobernanza ética integral en la arquitectura y en la experiencia de usuario:

1. **Aviso Explícito de IA en la Interfaz (Frontend):**  
   Se incluye un aviso visible en el formulario de tickets y un distintivo de estado en el encabezado indicando el modelo en uso (`Google Gemini` o `Groq Cloud`), con la advertencia clara de que la IA actúa como asistente de clasificación y no sustituye al técnico de soporte.
2. **Principio de Minimización de Datos (Art. 10 LOPDP):**  
   El formulario de ingreso solicita únicamente tres campos de contacto laboral: `nombre_cliente`, `email_cliente` y `codigo_abonado` (departamento/puesto). Queda terminantemente prohibida la solicitud de cédulas, datos biométricos, contraseñas o información sensible.
3. **Sanitización Preventiva de Contraseñas (Art. 23 LOPDP):**  
   Se implementa un filtro por expresiones regulares en `app/services/llm.py` que detecta y sustituye automáticamente cualquier contraseña o PIN por `[CONFIDENCIAL_REMOVIDO]` antes de persistir o transmitir datos al LLM.
4. **Compuerta Human-in-the-Loop Obligatoria (HITL):**  
   Ningún ticket se crea en firme en la base de datos ni se compromete el SLA sin la autorización explícita de un técnico o del propio colaborador tras revisar la sugerencia de autoatención.
5. **Cero Retención de Datos para Entrenamiento:**  
   Las llamadas a los proveedores externos de IA se realizan bajo políticas de no retención de datos para entrenamiento de modelos públicos.

---

## 3. Justificación y Beneficios
- **Conformidad Legal:** Cumplimiento pleno de la normativa ecuatoriana (LOPDP) y de los estándares éticos universitarios de UNIANDES.
- **Confianza del Colaborador:** El usuario comprende el funcionamiento del sistema, sabe que sus datos están protegidos y que siempre cuenta con el respaldo de un técnico humano.
- **Mitigación de Responsabilidad:** La empresa garantiza que la IA no toma decisiones autónomas de riesgo ni compromete contratos de forma descontrolada.

---

## 4. Consecuencias
- **Positivas:**
  - Sistema completamente auditable y éticamente defendible ante tribunales de titulación y entidades regulatorias.
  - Cero fugas de contraseñas hacia proveedores de nube o historiales de Git.

