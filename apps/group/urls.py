# _*_ coding: utf-8 _*_
__author__ = 'alan'
__date__ = '2018/3/13 下午3:23'

from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^$', GroupListView.as_view(), name="group_list"),
    url(r'^detail/(?P<group_id>\d+)/$', GroupDetailView.as_view(), name="group_detail"),
    url(r'^add/$', AddGroupView.as_view(), name="add_group"),
    url(r'^delete/$', DeleteGroupView.as_view(), name="delete_group"),

]