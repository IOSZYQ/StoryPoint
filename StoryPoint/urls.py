"""StoryPoint URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView
from project.views import ProjectListView
import xadmin

from users.views import *

urlpatterns = [
    # url('admin/', admin.site.urls),
    url('xadmin/', xadmin.site.urls),
    url('^$', ProjectListView.as_view(), name="index"),
    url('^login/', LoginView.as_view(), name="login"),
    url('^logout/', LogoutView.as_view(), name="logout"),
    url('^register/', RegiserView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),
    url(r'^add/', AddUserView.as_view(), name='add_user'),
    url(r'^delete/', AddUserView.as_view(), name='add_user'),

    #项目相关url配置
    url(r'^project/', include('project.urls', namespace="project")),

    #团队相关url配置
    url(r'^group/', include('group.urls', namespace="group")),

    # #绩效相关url配置
    url(r'^performance/', include('performance.urls', namespace="performance")),
]
