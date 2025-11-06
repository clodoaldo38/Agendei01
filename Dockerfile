FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

# Install system deps (optional: for future builds/extensions)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código para a imagem (necessário para Render)
COPY . /code/

# Variáveis padrão (podem ser sobrescritas em runtime)
ENV DJANGO_SETTINGS_MODULE=app.settings \
    DEBUG=0

# Coletar estáticos no build para servir via Whitenoise
RUN python manage.py collectstatic --noinput || true

# Executar migrações e iniciar Gunicorn usando a PORT do ambiente (Render)
CMD ["sh","-c","python manage.py migrate && gunicorn app.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3"]