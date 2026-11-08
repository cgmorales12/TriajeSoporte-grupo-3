# Dockerfile para Triaje Soporte Tecnológico PYME (Grupo 3 - UNIANDES)
# Versión fija de Python y usuario sin privilegios según OWASP / Rúbrica
FROM python:3.11.9-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Instalar dependencias del sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ingesta determinista del corpus oficial RAG en el contenedor
RUN python scripts/ingest.py || true

# Crear y cambiar a usuario sin privilegios (Seguridad OWASP)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

