# Generated by Django 3.1.7 on 2021-03-16 21:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_buytransactioncrypt'),
    ]

    operations = [
        migrations.AddField(
            model_name='buytransactioncrypt',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
