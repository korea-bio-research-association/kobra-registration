# Generated by Django 5.1.5 on 2025-01-30 03:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AddField(
            model_name='conference',
            name='event_type',
            field=models.CharField(choices=[('conference', 'Conference'), ('workshop', 'Workshop')], default='conference', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='orcid',
            field=models.CharField(blank=True, max_length=19),
        ),
        migrations.AddField(
            model_name='venue',
            name='photo',
            field=models.ImageField(blank=True, upload_to='.'),
        ),
        migrations.RemoveField(
            model_name='conference',
            name='organizers',
        ),
        migrations.CreateModel(
            name='Deadline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deadlines', to='main.conference')),
            ],
        ),
        migrations.CreateModel(
            name='EmailContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=1000)),
                ('body', models.TextField()),
                ('to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=1000)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='conference',
            name='organizers',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
