import json

from celery import shared_task
from requests import Session
from crypto_course.models import Crypt
from cryptocurrency.celery import app


@shared_task(name='appdata')
def data_app():
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '12263655-efc9-4238-803c-a1faeac698f6',
    }
    session = Session()
    session.headers.update(headers)
    response = session.get(url='https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest')
    data = json.loads(response.text)
    for i in range(len(data['data'])):
        Crypt.objects.filter(pk=845+i).update(price_crypt_dollar= data['data'][i]['quote']['USD']['price'])
        # app.conf.beat_schedule = {
        #     'add-every-60-seconds': {
        #         'task': 'tasks.data_app',
        #         'schedule': 60.0,
        #     },
        # }


