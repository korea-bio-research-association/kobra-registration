# Generated by Django 5.1 on 2025-03-09 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_abstractvote_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abstractvote',
            name='event',
        ),
    ]
