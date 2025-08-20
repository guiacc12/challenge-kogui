#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

python - <<'PY'
import os, socket, time
host = os.environ.get('POSTGRES_HOST', 'challenge_db')
port = int(os.environ.get('POSTGRES_PORT', '5432'))
print(f"🟡 Waiting for Postgres Database Startup ({host} {port}) ...")
while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            break
    except OSError:
        time.sleep(2)
print(f"✅ Postgres Database Started Successfully ({host}:{port})")
PY

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
gunicorn challenge_web.wsgi:application --bind 0.0.0.0:8000