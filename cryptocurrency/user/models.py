from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from crypto_course.models import CryptoWallet, Crypt
from datetime import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='image/users', verbose_name='Изображение')
    user_balance = models.FloatField(blank=True, default=0, verbose_name='Баланс')

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профиль"

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class BuyTransactionCrypt(models.Model):
    from_user = models.ForeignKey(CryptoWallet, related_name='+', on_delete=models.CASCADE)
    from_user_value = models.FloatField(blank=True, verbose_name='Сума отправителя')
    date = models.DateTimeField(default=datetime.now, blank=True)
    to_crypt = models.ForeignKey(Crypt, related_name='+', on_delete=models.CASCADE)
    to_crypt_wallet = models.ForeignKey(CryptoWallet, on_delete=models.CASCADE)
    to_crypt_value = models.FloatField(blank=True, verbose_name='сумма получателя')

    class Meta:
        verbose_name = "Транзакция покупки"
        verbose_name_plural = "Транзакции покупки"

    def __str__(self):
        return self.from_user


class Sell_Transaction_Crypt(models.Model):
    from_user = models.ForeignKey(User, related_name='from+', on_delete=models.CASCADE)
    from_crypt = models.ForeignKey(Crypt, related_name='+', on_delete=models.CASCADE)
    from_crypt_wallet = models.ForeignKey(CryptoWallet, related_name='+', on_delete=models.CASCADE)
    from_crypt_value = models.FloatField(blank=True, verbose_name='Сума продажи')
    date = models.DateTimeField(default=datetime.now, blank=True)
    to_user = models.ForeignKey(User, related_name='to+', on_delete=models.CASCADE)
    to_value = models.FloatField(blank=True, verbose_name='Сума покупки')

    class Meta:
        verbose_name = 'Транзакция продажи'
        verbose_name_plural = 'Транзакции продажи'

    def __str__(self):
        return self.from_user


class Wallet_Transaction_Crypt(models.Model):
    from_user = models.ForeignKey(User, related_name='from+', on_delete=models.CASCADE)
    from_crypt = models.ForeignKey(Crypt, related_name='fromcrypt+', on_delete=models.CASCADE)
    from_crypt_wallet = models.ForeignKey(CryptoWallet, related_name='fromwalley+', on_delete=models.CASCADE)
    from_crypt_value = models.FloatField(blank=True, verbose_name='Сума продажи')
    date = models.DateTimeField(default=datetime.now, blank=True)
    to_user = models.ForeignKey(User, related_name='from+', on_delete=models.CASCADE)
    to_crypt = models.ForeignKey(Crypt, related_name='toctypt+', on_delete=models.CASCADE)
    to_crypt_wallet = models.ForeignKey(CryptoWallet, related_name='towallet+', on_delete=models.CASCADE)
    to_crypt_value = models.FloatField(blank=True, verbose_name='Сума продажи')

    class Meta:
        verbose_name = 'Транзакция перевода'
        verbose_name_plural = 'Транзакции переводов'

    def __str__(self):
        return self.from_user