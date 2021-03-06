# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-27 19:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mycritic_app', '0005_auto_20170427_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('identifier', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('poster', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('identifier', models.AutoField(primary_key=True, serialize=False)),
                ('rating_val', models.FloatField(default=0)),
                ('movie_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycritic_app.Movie')),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='id',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rating',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycritic_app.UserProfile'),
        ),
    ]
