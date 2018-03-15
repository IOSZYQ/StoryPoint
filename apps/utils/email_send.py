# _*_ coding: utf-8 _*_
__author__ = 'alan'
__date__ = '2018/3/8 下午2:53'

from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from StoryPoint.settings import EMAIL_FROM

def random_str(randomlength=8):
    str=''
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWSYZabcdefghijklmnopqrstuvwxyz0123456789'
    lenth = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, lenth)]
    return str

def send_sp_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.email = email
    email_record.code = code
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""


    if send_type == "register":
        email_title = "路书SP系统注册激活链接"
        email_body = "请点击下面的链接激活你的帐号:http://127.0.0.1:8000/active/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    if send_type == "forget":
        email_title = "路书SP系统重置密码链接"
        email_body = "请点击下面的链接重置你的密码:http://127.0.0.1:8000/reset/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass