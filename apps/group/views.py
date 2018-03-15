from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

from .models import *
# Create your views here.

class GroupListView(View):
    def get(self, request):
        return render(request, 'goupList.html', {})


class GroupDetailView(View):
    def get(self, request, group_id):
            group = Group.objects.get(id=group_id)
            if group:
                return render(request, 'detail.html', {
                    "project":group
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

