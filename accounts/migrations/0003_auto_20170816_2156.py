# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-16 19:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_auto_20170812_2052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='invited',
        ),
        migrations.RemoveField(
            model_name='friend',
            name='sender',
        ),
        migrations.AddField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(related_name='friends', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Friend',
        ),
    ]
