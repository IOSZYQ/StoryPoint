# _*_ coding: utf-8 _*_
__author__ = 'alan'
__date__ = '2018/3/10 下午3:55'

from django.conf.urls import url, include

from .views import *

taskUrlPatterns = [
    url(r'^add/$', CreateEditTaskInfoView.as_view(), name="add_task"),
    url(r'^edit/$', CreateEditTaskInfoView.as_view(), name="edit_task"),
    url(r'^edit_detail/$', EditTaskDetailView.as_view(), name="edit_task_detail"),
    url(r'^delete/$', deleteTaskView.as_view(), name="delete_task"),
]

urlpatterns = [
    url(r'^$', ProjectListView.as_view(), name="project_list"),
    url(r'^detail/(?P<project_id>\d+)/$', ProjectDetailView.as_view(), name="project_detail"),
    url(r'^add/$', CreateEditProjectInfoView.as_view(), name="add_project"),
    url(r'^edit/$', CreateEditProjectInfoView.as_view(), name="edit_project"),
    url(r'^edit_detail/$', EditorProjectDetailView.as_view(), name="edit_project_detail"),
    url(r'^delete/$', deleteProjectView.as_view(), name="delete_project"),

    url(r'^gettask/(?P<task_id>\d+)$', getTask.as_view(), name="task_info"),

    url(r'task/', include(taskUrlPatterns, namespace='project_task'))
]