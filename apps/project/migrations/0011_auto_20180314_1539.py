# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-03-14 15:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_auto_20180314_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persontask',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_user', to=settings.AUTH_USER_MODEL, verbose_name='任务完成人'),
        ),
    ]
