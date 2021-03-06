# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-03-21 15:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20180321_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='expect_end_time',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2018, 3, 21, 15, 57, 1, 933502), verbose_name='预计终止时间'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='end_time',
            field=models.DateField(auto_now_add=True, verbose_name='实际终止时间'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('executing', '执行'), ('acceptance', '验收'), ('release', '发布'), ('suspend', '滞后')], default='executing', max_length=15),
        ),
    ]
