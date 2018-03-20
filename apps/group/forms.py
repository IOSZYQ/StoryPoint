# _*_ coding: utf-8 _*_
__author__ = 'alan'
__date__ = '2018/3/19 下午5:32'
from django import forms


from .models import Group

class AddGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
