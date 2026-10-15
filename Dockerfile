FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

# Producción (Railway): aplica migraciones, carga datos de prueba y arranca gunicorn.
# Las migraciones se generan a mano (makemigrations) y se suben al repo.
CMD ["sh", "-c", "python manage.py migrate && python manage.py seed_logica && gunicorn config.wsgi --bind 0.0.0.0:${PORT:-8000}"]
