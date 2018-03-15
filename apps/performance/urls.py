# _*_ coding: utf-8 _*_
__author__ = 'alan'
__date__ = '2018/3/13 下午2:58'

from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^$', PerformanceView.as_view(), name="performance"),
    url(r'^user_list/$', UserListPerformanceView.as_view(), name="user_performance_list"),
    url(r'^user_detail/(?P<project_id>\d+)/$', UserPerformanceView.as_view(), name="user_performance_detail"),
    url(r'^group_detail/(?P<project_id>\d+)/$', GroupPerformanceView.as_view(), name="group_performance_detail"),
    url(r'^department_detail/(?P<project_id>\d+)/$', DepartmentPerformanceView.as_view(), name="department_performance_detail"),

]