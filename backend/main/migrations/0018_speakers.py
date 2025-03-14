# Generated by Django 5.1 on 2025-03-08 03:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_remove_user_orcid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Speakers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('email', models.EmailField(max_length=254)),
                ('affiliation', models.CharField(blank=True, max_length=1000)),
                ('is_domestic', models.BooleanField(default=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='speakers', to='main.event')),
            ],
        ),
    ]
