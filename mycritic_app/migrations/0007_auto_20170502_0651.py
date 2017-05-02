# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-02 10:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mycritic_app', '0006_auto_20170427_1533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='rating_val',
        ),
        migrations.AddField(
            model_name='rating',
            name='rating',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='rating',
            name='movie_id',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='rating',
            name='user_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(max_length=150, primary_key=True, serialize=False),
        ),
    ]
