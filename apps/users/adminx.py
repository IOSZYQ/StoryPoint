# _*_ coding: utf-8 _*_
__author__ = 'alan'
__date__ = '2018/3/7 下午2:39'

import xadmin
from .models import *
from xadmin import views
from xadmin.plugins.auth import UserAdmin

# class BaseSetting(object):
#     enable_themes = True
#     use_bootswatch = True

class GlobalSettings(object):
    site_title = "路书SP管理系统"
    site_footer = "路书(北京)科技有限公司"
    menu_style = "accordion"


# class UserProfileAdmin(UserAdmin):
#     list_display = ['username', 'group', 'email', 'is_staff', 'is_active', 'nick_name', 'date_joined', 'birday', 'gender', 'address', 'mobile', 'image']
#     search_fields = ['username', 'group', 'email', 'is_staff', 'is_active', 'nick_name', 'birday', 'gender', 'address', 'mobile', 'image']
#     list_filter = ['username', 'group', 'email', 'is_staff', 'is_active', 'nick_name', 'date_joined', 'birday', 'gender', 'address', 'mobile', 'image']

class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']



# xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
# xadmin.site.register(UserProfile, UserProfileAdmin)
