# Generated by Django 5.1 on 2025-03-08 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_speaker_type_alter_speaker_is_domestic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='venue',
            field=models.CharField(max_length=1000),
        ),
        migrations.DeleteModel(
            name='Venue',
        ),
    ]
