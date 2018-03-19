from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from json import dumps

from .models import *
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
            if group.leader.id != None and len(users) != 0:
                users = sorted(users, key=lambda user:user.id!=group.leader.id)
            if group:
                return render(request, 'team-detail.html', {
                    "group":group,
                    "users":users
                })

class AddGroupView(View):
    def post(self, request):
        name = request.POST.get('teamName','')
        id = request.POST.get('teamId', '')
        if name != '':
            if id != '':
                group = Group.object.get(pk=id)
                if group != None:
                    group.name = name
                    group.save()
                    return HttpResponse(dumps({'status': 0}), content_type='application/json')
                else:
                    result = {'status': -1, 'msg': 'id错误'}
                    return HttpResponse(dumps(result), content_type='application/json')
            else:
                group = Group.objects.create.init(name=name)
                group.save()
                return HttpResponse(dumps({'status': 0}), content_type='application/json')
        else:
            result = {'status': -1, 'msg':'名字不能为空'}
            return HttpResponse(dumps(result), content_type='application/json')

class DeleteGroupView(View):
    def post(self, request):
        group_id = request.POST.get('group_id', '')
        group = Group.objects.get(pk=group_id)
        group.delete()
        return HttpResponse("{'status':'success}")

