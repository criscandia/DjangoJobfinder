from __future__ import absolute_import, unicode_literals

# Esto asegurará que la aplicación Celery se cargue siempre que
# Django se inicie para el uso compartido de esta aplicación.
from .celery import app as celery_app

__all__ = ("celery_app",)
