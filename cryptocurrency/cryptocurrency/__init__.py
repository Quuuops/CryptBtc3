from __future__ import absolute_import
from .celery import app as celery_app
# Подключаем объект
__all__ = ('celery_app',)
