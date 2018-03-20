# _*_ coding: utf-8 _*_
__author__ = 'alan'
__date__ = '2018/3/13 下午2:30'

from django.conf.urls import url, include

from users.views import *

urlpatterns = [
    url('^login/', LoginView.as_view(), name="login"),
    url('^logout/', LogoutView.as_view(), name="logout"),
    url('^register/', RegiserView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),
    url(r'^add/', AddUserView.as_view(), name='add_user'),
    url(r'^delete/', AddUserView.as_view(), name='add_user'),
]