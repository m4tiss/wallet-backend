# Generated by Django 5.1.7 on 2025-04-15 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bonds', '0003_userbond_isactive'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userbond',
            old_name='isActive',
            new_name='is_active',
        ),
    ]
