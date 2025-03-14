# Generated by Django 5.1 on 2025-03-03 15:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_event_accepts_abstract'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abstract',
            name='abstract',
        ),
        migrations.AddField(
            model_name='abstract',
            name='file_path',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='abstract',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='abstract',
            name='is_oral',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='AbstractReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('comment', models.TextField(blank=True)),
                ('abstract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='main.abstract')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reviewers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewers', to='main.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
