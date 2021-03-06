# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-03-15 21:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manager_projects', to=settings.AUTH_USER_MODEL, verbose_name='项目经理'),
        ),
        migrations.AddField(
            model_name='persontask',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='person_task', to='project.Task', verbose_name='小组任务'),
        ),
        migrations.AddField(
            model_name='persontask',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_user', to=settings.AUTH_USER_MODEL, verbose_name='任务完成人'),
        ),
    ]
