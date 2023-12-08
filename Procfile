web: gunicorn conf.wsgi --capture-output --log-level info
worker: python manage.py run_huey
release: python manage.py migrate