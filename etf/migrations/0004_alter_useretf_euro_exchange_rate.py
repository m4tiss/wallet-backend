# Generated by Django 5.1.7 on 2025-04-21 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etf', '0003_useretf_euro_exchange_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useretf',
            name='euro_exchange_rate',
            field=models.DecimalField(decimal_places=4, default=4.2, max_digits=10),
        ),
    ]
