from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from json import dumps

from .models import *
from .forms import AddGroupForm
# Create your views here.

class GroupListView(View):
    def get(self, request):
        groups = Group.objects.all()
        return render(request, 'team.html', {
            'groups':groups
        })


class GroupDetailView(View):
    def get(self, request, group_id):
            group = Group.objects.get(id=group_id)
            users = group.members.all()
            if group.leader != None and len(users) != 0:
                users = sorted(users, key=lambda user:user.id!=group.leader.id)
            if group:
                return render(request, 'team-detail.html', {
                    "group":group,
                    "users":users
                })

class AddGroupView(View):
    def post(self, request):
        add_group_form = AddGroupForm(request.POST)
        if add_group_form.is_valid():
            name = request.POST.get('name', '')
            id = request.POST.get('id', '')
            if int(id) != 0:
                group = Group.objects.get(pk=id)
                if group != None:
                    group.name = name
                    group.save()
                    return HttpResponse(dumps({'status': 0}), content_type='application/json')
                else:
                    result = {'status': -1, 'msg': 'id错误'}
                    return HttpResponse(dumps(result), content_type='application/json')
            else:
                if Group.objects.filter(name=name):
                    return HttpResponse(dumps({'status':-1,'msg':'小组名字已被占用,请更换名字'}))
                group = Group.objects.create(name=name)
                group.save()
                return HttpResponse(dumps({'status': 0}), content_type='application/json')
        else:
            result = {'status': -1, 'msg': '名字不能为空'}
            return HttpResponse(dumps(result), content_type='application/json')

class DeleteGroupView(View):
    def post(self, request):
        group_id = request.POST.get('id', '')
        group = Group.objects.filter(pk=group_id).last()
        if group != None:
            group.delete()
        result = {'status': 0}
        return HttpResponse(dumps(result), content_type='application/json')

class AllGroupView(View):
    def get(self, request):
        dic = []
        for group in Group.objects.all():
            dic.append({'id':group.id,'name':group.name})
        result = {'status': 0,'result':dic}
        return HttpResponse(dumps(result), content_type='application/json')


