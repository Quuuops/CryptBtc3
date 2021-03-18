# Generated by Django 3.1.7 on 2021-03-17 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_course', '0008_auto_20210308_1430'),
        ('user', '0020_wallet_transaction_crypt'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet_transaction_crypt',
            name='to_crypt_wallet',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='towallet+', to='crypto_course.cryptowallet'),
            preserve_default=False,
        ),
    ]