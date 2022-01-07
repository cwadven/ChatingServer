web: gunicorn --bind :8000 --workers=2 --threads=15 config.wsgi:application
websocket: daphne -b :: -p 5000 config.asgi:application