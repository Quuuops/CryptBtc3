# Generated by Django 3.1.7 on 2021-03-08 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_course', '0005_auto_20210308_0324'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crypt',
            old_name='user',
            new_name='wallet',
        ),
        migrations.RenameField(
            model_name='cryptowallet',
            old_name='name_crypt',
            new_name='user',
        ),
    ]
