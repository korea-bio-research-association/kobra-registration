# Generated by Django 5.1 on 2025-03-10 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_alter_event_capacity_abstract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='max_votes',
            field=models.IntegerField(null=True),
        ),
    ]
