# Generated by Django 5.1 on 2025-03-10 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_remove_abstractvote_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='capacity_abstract',
            field=models.IntegerField(null=True),
        ),
    ]
