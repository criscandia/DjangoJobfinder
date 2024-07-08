from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establece el valor predeterminado de la variable de entorno DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobfinder.settings")

app = Celery("jobfinder")

# Namespace 'CELERY' significa que todas las configuraciones relacionadas con celery
# deben tener un prefijo 'CELERY_' en el archivo settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Descubre y carga tareas de todas las aplicaciones de Django registradas en INSTALLED_APPS
app.autodiscover_tasks()
