# Generated by Django 5.1 on 2025-03-08 09:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_speakers'),
    ]

    operations = [
        migrations.AddField(
            model_name='customanswer',
            name='reference',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.customquestion'),
        ),
    ]
