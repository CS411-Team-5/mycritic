# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-27 15:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mycritic_app', '0004_userprofile_movies_rated'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='user_name',
            new_name='username',
        ),
    ]