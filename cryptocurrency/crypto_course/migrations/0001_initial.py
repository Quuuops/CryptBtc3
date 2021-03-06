# Generated by Django 3.1.7 on 2021-03-04 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crypt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank='True', upload_to='photo', verbose_name='Фото')),
                ('name_crypt', models.CharField(max_length=50)),
                ('symbol_crypt', models.CharField(max_length=5, verbose_name='Сокращенно')),
                ('price_crypt_dollar', models.FloatField(blank=True, null=True, verbose_name='Цена')),
                ('percent', models.FloatField(blank=True, null=True, verbose_name='Процент')),
            ],
            options={
                'verbose_name': 'Крипто валюта',
                'verbose_name_plural': 'Крипто валюты',
            },
        ),
    ]
