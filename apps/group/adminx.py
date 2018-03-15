# _*_ coding: utf-8 _*_
__author__ = 'alan'
__date__ = '2018/3/13 下午3:32'

import xadmin
from .models import *

class GroupAdmin(object):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']


xadmin.site.register(Group, GroupAdmin)
