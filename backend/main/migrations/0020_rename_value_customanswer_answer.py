# Generated by Django 5.1 on 2025-03-08 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_customanswer_reference'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customanswer',
            old_name='value',
            new_name='answer',
        ),
    ]
