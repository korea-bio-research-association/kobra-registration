# Generated by Django 5.1 on 2025-03-08 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_event_abstract_deadline_event_registration_deadline_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='event_type',
        ),
    ]
