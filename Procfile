release: python retail_alerts/manage.py migrate
web: gunicorn --pythonpath retail_alerts retail_alerts.wsgi --log-file=-