# Generated by Django 3.1.7 on 2021-03-17 18:38

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_course', '0008_auto_20210308_1430'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0019_auto_20210317_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet_Transaction_Crypt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_crypt_value', models.FloatField(blank=True, verbose_name='Сума продажи')),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('from_crypt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fromcrypt+', to='crypto_course.crypt')),
                ('from_crypt_wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fromwalley+', to='crypto_course.cryptowallet')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from+', to=settings.AUTH_USER_MODEL)),
                ('to_crypt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='toctypt+', to='crypto_course.crypt')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Транзакция перевода',
                'verbose_name_plural': 'Транзакции переводов',
            },
        ),
    ]
