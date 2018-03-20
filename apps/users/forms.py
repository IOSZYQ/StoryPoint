# _*_ coding: utf-8 _*_
__author__ = 'alan'
__date__ = '2018/3/7 下午9:18'
from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)

class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(required=True, min_length=6)
    captcha = CaptchaField(error_messages={"invalid":"验证码错误"})

class ForgetForm(forms.Form):
    email = forms.EmailField()
    # captcha = CaptchaField(error_messages={"invalid":"验证码错误"})

class ModifyPwdForm(forms.Form):
    oldpassword  = forms.CharField(required=True, min_length=6)
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)

class AddForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username','email']
