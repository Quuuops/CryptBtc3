from __future__ import absolute_import, unicode_literals
import os
from time import sleep
from django.conf import settings
# Из только что установленной библиотеки celery импортируем класс Celery
from celery import Celery
from django.conf import settings

# Указываем где находится модуль django и файл с настройками django (имя_вашего_проекта.settings)
# в свою очередь в файле settings будут лежать все настройки celery.
# Соответственно при указании данной директивы нам не нужно будет при вызове каждого task(функции) прописывать
# эти настройки.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptocurrency.settings')
# Создаем объект(экземпляр класса) celery и даем ему имя
app = Celery('cryptocurrency', namespace='CELERY', include=['user.tasks'])
# Загружаем config с настройками для объекта celery.
# т.е. импортируем настройки из django файла settings
# namespace='CELERY' - в данном случае говорит о том, что применятся будут только
# те настройки из файла settings.py которые начинаются с ключевого слова CELERY
app.config_from_object('django.conf:settings')

# В нашем приложении мы будем создавать файлы tasks.py в которых будут находится
# task-и т.е. какие-либо задания. При указании этой настройки
# celery будет автоматом искать такие файлы и подцеплять к себе.
app.autodiscover_tasks()



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    'task_data': {
        'task': 'appdata',
        'schedule': 60 * 4,
    }, }
