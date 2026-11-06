# ADR-004: Adopción de SQLite Parametrizado, Ciclo de Vida del Contenedor y Estrategia de Persistencia
**Estado:** Aceptado  
**Fecha:** Octubre 2026 (Actualizado Noviembre 2026)  
**Autores:** Christian Morales, Luis Fernando Ribera, Amalia Geoconda Iguasnia  

## 1. Contexto y Clasificación del Ciclo de Vida de los Datos
En el despliegue del sistema dentro de microcontenedores Linux (Docker / Render Cloud), el contenedor «nace limpio en cada arranque». Por ello, la arquitectura desacopla estrictamente los datos en tres categorías operativas:

1. **Datos de Solo Lectura («Viven dentro de la imagen»):**
   - El índice vectorial persistente de RAG (`data/chroma/`).
   - El corpus de 15 manuales técnicos en Markdown (`data/raw/`).
   - Las configuraciones deterministas de negocio (`config/matriz_prioridad.json`, `config/tarifas.json`, `config/parametros.yaml`).
   - *Decisión:* Se copian directamente en la imagen de Docker durante el build (`COPY . .`), garantizando que la aplicación arranque inmediatamente sin descargas externas, sin costos de red y lista para resolver consultas RAG desde el segundo cero.

2. **Datos Transaccionales Efímeros del MVP («Se escribe y se acepta el ciclo efímero»):**
   - El historial de tickets de soporte y bitácora de auditoría transaccional (`data/conectatec.db`).
   - *Decisión:* Para el prototipo funcional y la sustentación académica (despliegue en contenedor único de Render, réplicas = 1), se utiliza SQLite embebido. Se acepta que el contenedor nazca limpio en cada reinicio o redepliegue de versión, eliminando dependencias de infraestructura de pago o tarjetas de crédito.

3. **Datos Transaccionales de Producción («Se escribe e importa a largo plazo»):**
   - En un entorno corporativo con múltiples instancias horizontales, los tickets deben persistir en un servicio de base de datos externa gestionada (PostgreSQL / Supabase / Neon) o en un volumen persistente compartido (Render Persistent Disk / AWS EFS).

---

## 2. Pregunta de Arquitectura: «¿Qué ve el usuario si hay dos copias de la app, cada una con su SQLite?»
Si un balanceador de carga distribuye tráfico entre dos réplicas concurrentes (Instancia A e Instancia B) utilizando SQLite local en disco efímero:
- **Efecto Observado:** El usuario experimenta **inconsistencia severa de datos (Split-Brain / Estado Fragmentado)**.
- **Ejemplo Operativo:** Si la petición HTTP de creación de ticket llega a la Instancia A, el ticket se registra en el archivo `conectatec.db` de A. Si la siguiente petición (por ejemplo, recargar el tablero Kanban en `/tablero`) es despachada por el balanceador hacia la Instancia B, el usuario no verá el ticket creado, porque la base de datos de B es completamente independiente y desconoce los registros de A.
- **Mitigación Arquitectónica:**
  - Para el MVP: Concurrencia controlada en una única instancia activa (`replicas: 1`).
  - Para Producción: Desacoplamiento de SQLite hacia una base de datos relacional externa centralizada (PostgreSQL), para la cual los repositorios de `app/database.py` ya están preparados.

---

## 3. Justificación de SQLite en el MVP
1. **Cero Fricción de Despliegue:** Funciona de forma autónoma en cualquier entorno (Windows, Linux, macOS, Docker) sin requerir instalación de servicios adicionales.
2. **Seguridad contra Inyecciones SQL (OWASP):** Se utilizan consultas estrictamente parametrizadas con marcadores de posición (`?`), neutralizando cualquier riesgo de inyección SQL.
3. **Latencia Ultrabaja:** Consultas y escrituras en memoria/disco local en menos de 1 milisegundo (sin sobrecarga de red).

---

## 4. Consecuencias
- Para el seminario y la demostración en vivo, SQLite satisface plenamente la integridad transaccional requerida con costo cero ($0.00).
- La arquitectura mantiene el principio de desacoplamiento para migrar a PostgreSQL modificando exclusivamente el motor de conexión en `app/database.py`.
