# ADR-007: Gestión de Credenciales en Variables de Entorno y Perímetro de Cero Secretos
**Estado:** Aceptado  
**Fecha:** Octubre 2026  
**Autores:** Christian Morales, Luis Fernando Ribera, Amalia Geoconda Iguasnia  

## Contexto
La filtración accidental de API Keys o credenciales en repositorios de Git representa una de las vulnerabilidades críticas más frecuentes (OWASP LLM06 / OWASP LLM07). Asimismo, la legislación ecuatoriana (LOPDP) sanciona la persistencia o exposición de contraseñas de usuarios.

## Decisión
1. Prohibir de manera absoluta la escritura de claves en código fuente o commits de Git.
2. Aplicar la regla de oro: **«El .env no viaja: la caja fuerte sí»**:
   - **En la máquina local:** El archivo `.env` permanece fuera de Git mediante `.gitignore` y fuera de la caja de construcción del contenedor mediante `.dockerignore`.
   - **En la nube:** Las claves nunca se empaquetan en la imagen Docker. La caja fuerte de la plataforma (Environment Variables / Secret Manager) almacena las claves cifradas y las entrega en tiempo de ejecución al microcontenedor como variables de entorno del sistema operativo (`os.environ`).
3. Mantener `.env.example` exclusivamente con valores vacíos para orientación de evaluadores.
4. Desarrollar un script automatizado de auditoría (`scripts/auditar_cero_secretos.py`) que verifique el árbol de Git antes de cada entrega.
5. Anonimizar contraseñas en reportes de usuarios mediante expresiones regulares antes de persistir o enviar al LLM.

## Justificación
1. **Cumplimiento Legal y Normativo:** Garantiza el respeto a la LOPDP y a las directrices de ciberseguridad del seminario.
2. **Auditoría Verificable:** La ejecución de `python scripts/auditar_cero_secretos.py` otorga un reporte de 100% de cumplimiento en segundos.

## Consecuencias
- Imposibilidad de filtración de claves en GitHub incluso si el repositorio es público.
