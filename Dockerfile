FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput && mkdir -p /data && chmod 777 /data
ENV DJANGO_DB_PATH=/data/db.sqlite3
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn django_concert.wsgi:application --bind 0.0.0.0:8000"]
