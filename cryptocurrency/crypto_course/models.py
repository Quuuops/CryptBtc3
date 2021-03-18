from django.db import models
from django.contrib.auth.models import User


class Crypt(models.Model):
    photo_crypt = models.ImageField(upload_to='photo', verbose_name='Фото', blank='True')
    name_crypt = models.CharField(max_length=50)
    symbol_crypt = models.CharField(max_length=10, verbose_name='Сокращенно')
    price_crypt_dollar = models.FloatField(blank=True, null=True, verbose_name='Цена')
    percent = models.FloatField(blank=True, null=True, verbose_name='Процент')

    def __str__(self):
        return self.name_crypt

    class Meta:
        verbose_name = "Крипто валюта"
        verbose_name_plural = "Крипто валюты"


class CryptoWallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypt = models.ForeignKey(Crypt, on_delete=models.CASCADE)
    wallet = models.CharField(max_length=50, verbose_name='Кошелек')
    value_crypt = models.FloatField(default=0, verbose_name='Сумма')

    def __str__(self):
        return self.wallet

    class Meta:
        verbose_name = "Кошелек"
        verbose_name_plural = "Кошельки"
