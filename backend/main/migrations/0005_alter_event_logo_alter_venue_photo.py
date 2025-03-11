# Generated by Django 5.1.5 on 2025-01-30 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_session_chairs_alter_preference_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='logo',
            field=models.ImageField(blank=True, upload_to='./media/event'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='photo',
            field=models.ImageField(blank=True, upload_to='./media/venue'),
        ),
    ]
