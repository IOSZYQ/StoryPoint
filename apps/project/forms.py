# _*_ coding: utf-8 _*_
__author__ = 'alan'
__date__ = '2018/3/12 下午8:28'

from django import forms
from project.models import *

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['manager', 'name', 'sp', 'weight', 'impression', 'acceptance_serious_bug', 'acceptance_medium_bug', 'acceptance_slight_bug', 'release_serious_bug', 'release_medium_bug', 'release_slight_bug', 'status']

        def clean_weight(self):
            weight = self.cleaned_data['weight']
            if int(weight) > 0 & int(weight) < 2:
                return weight
            else:
                raise forms.ValidationError("权重必须大于零且小于等于2", code="weight_invalid")

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status', 'description', 'gsp']