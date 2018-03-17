from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

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

        return HttpResponse("{'status':'success}")

class DeleteGroupView(View):
    def post(self, request):
        group_id = request.POST.get('group_id', '')
        group = Group.objects.get(pk=group_id)
        group.delete()
        return HttpResponse("{'status':'success}")

