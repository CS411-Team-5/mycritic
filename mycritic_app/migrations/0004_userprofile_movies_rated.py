# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-27 15:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycritic_app', '0003_auto_20170427_0755'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='movies_rated',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
