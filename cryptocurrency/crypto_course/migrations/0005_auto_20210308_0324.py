# Generated by Django 3.1.7 on 2021-03-08 03:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crypto_course', '0004_auto_20210308_0107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crypt',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crypto_course.cryptowallet'),
        ),
        migrations.AlterField(
            model_name='cryptowallet',
            name='name_crypt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
