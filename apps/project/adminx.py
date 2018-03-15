# _*_ coding: utf-8 _*_
__author__ = 'alan'
__date__ = '2018/3/7 下午2:55'

import xadmin
from .models import *

class ProjectAdmin(object):
    list_display = ['name','manager','create_time', 'start_time', 'end_time', 'executing', 'acceptance','sp','weight','impression','acceptance_serious_bug','acceptance_medium_bug','acceptance_slight_bug','release_serious_bug','release_medium_bug','release_slight_bug','status']
    search_fields = ['name','manager', 'executing', 'acceptance','sp','weight','impression','acceptance_serious_bug','acceptance_medium_bug','acceptance_slight_bug','release_serious_bug','release_medium_bug','release_slight_bug','status']
    list_filter = ['name','manager','create_time', 'start_time', 'end_time', 'executing', 'acceptance','sp','weight','impression','acceptance_serious_bug','acceptance_medium_bug','acceptance_slight_bug','release_serious_bug','release_medium_bug','release_slight_bug','status']

xadmin.site.register(Project, ProjectAdmin)

class TaskAdmin(object):
    list_display = ['project', 'group', 'status', 'description', 'gsp']
    search_fields = ['project', 'group', 'status', 'description', 'gsp']
    list_filter = ['project', 'group', 'status', 'description', 'gsp']
xadmin.site.register(Task, TaskAdmin)

class PersonTaskAdmin(object):
    list_display = ['user', 'psp', 'task']
    search_fields = ['user', 'psp', 'task']
    list_filter = ['user', 'psp', 'task']
xadmin.site.register(PersonTask, PersonTaskAdmin)