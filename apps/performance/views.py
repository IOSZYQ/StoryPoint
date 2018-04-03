from django.shortcuts import render
from django.views.generic.base import View
from datetime import datetime, timedelta,date
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse

import re

from users.models import UserProfile
from group.models import Group
from project.models import Project,Task,PersonTask
# Create your views here.

class PerformanceView(View):
    def get(self, request):
        startyear = request.GET.get('startyear', '2018')
        startmonth = request.GET.get('startmonth', '1')
        endyear = request.GET.get('endyear', '2018')
        endmonth = request.GET.get('endmonth', '12')
        start = getMonthFirstDay(year=int(startyear), month=int(startmonth))
        end = getNextMonthFirstDay(year=int(endyear), month=int(endmonth))
        all_project = Project.objects.filter(end_time__range=[start, end],status='finish')
        months = (int(endmonth) - int(startmonth)) + 1 + (int(endyear) - int(startyear))*12
        if months < 1:
            months = 1
        time = "{0}.{1}-{2}.{3}".format(startyear, startmonth, endyear,endmonth)
        data = {"0" : 0}
        result = [{'id':'0', 'jx':0, 'name':'产品研发部'}]
        for group in Group.objects.all():
            data['{0}'.format(group.id)] = 0
            result.append({'id':'{0}'.format(group.id), 'jx':0, 'name':group.name})
        for project in all_project:
            data["0"] += project.getSP()
            for task in project.project_task.all():
                data['{0}'.format(task.group.id)] += task.getSP()
        for dic in result:
            jx = round((data[dic['id']]/months/5) if(dic['id'] == '0') else (data[dic['id']]/months),1)
            if jx > 100:
                jx = 100
            dic['jx'] = jx
        kpiurl = reverse('performance:performance')
        return render(request, 'kpi-team.html', {
            "result": result,
            "time":time,
            'url':kpiurl,
            "startyear":startyear,
            "startmonth":startmonth,
            "endyear":endyear,
            "endmonth":endmonth})

class UserListPerformanceView(View):
    def get(self, request):
        startyear = request.GET.get('startyear', '2018')
        startmonth = request.GET.get('startmonth', '1')
        endyear = request.GET.get('endyear', '2018')
        endmonth = request.GET.get('endmonth', '12')
        start = getMonthFirstDay(year=int(startyear), month=int(startmonth))
        end = getNextMonthFirstDay(year=int(endyear), month=int(endmonth))
        all_project = Project.objects.filter(end_time__range=[start, end],status='finish')
        months = (int(endmonth) - int(startmonth)) + 1 + (int(endyear) - int(startyear)) * 12
        if months < 1:
            months = 1
        time = "{0}.{1}-{2}.{3}".format(startyear, startmonth, endyear, endmonth)

        data = {}
        result = []
        for user in UserProfile.objects.all():
            data[str(user.id)] = 0
            result.append({"id":str(user.id), 'name':user.username, 'jx':0})
        for project in all_project:
            if project.manager != None:
                data[str(project.manager.id)] += project.getManagerSP()
            for task in project.project_task.all():
                if task.group.leader != None:
                    data[str(task.group.leader.id)] += task.getGroupLeaderSP()
                for person_task in task.person_task.all():
                    data[str(person_task.user.id)] += person_task.getSP()
        for dic in result:
            jx = round(data[dic['id']]/months,1)
            if jx > 100:
                jx = 100
            dic['jx'] = jx

        result = sorted(result, key=lambda user: user["jx"])
        result.reverse()
        kpiurl = reverse('performance:user_list')
        return render(request, 'kpi-person.html', {
            'result':result,
            'time':time,
            'url':kpiurl,
            "startyear":startyear,
            "startmonth":startmonth,
            "endyear":endyear,
            "endmonth":endmonth})

class DepartmentPerformanceView(View):
    def get(self, request):
        startyear = request.GET.get('startyear', '2018')
        startmonth = request.GET.get('startmonth', '1')
        endyear = request.GET.get('endyear', '2018')
        endmonth = request.GET.get('endmonth', '12')
        start = getMonthFirstDay(year=int(startyear), month=int(startmonth))
        end = getNextMonthFirstDay(year=int(endyear), month=int(endmonth))
        all_project = Project.objects.filter(end_time__range=[start, end],status='finish')
        months = (int(endmonth) - int(startmonth)) + 1 + (int(endyear) - int(startyear)) * 12
        if months < 1:
            months = 1
        sp = 0
        for project in all_project:
            sp += project.getSP()
        sp = round(sp, 1)
        score = round(sp/months/5,1)
        if score > 100:
            score = 100
        kpiurl = reverse('performance:department')
        return render(request, 'kpi-detail-department.html', {
            'sp':sp,
            'all_project':all_project,
            'score':score,
            'url':kpiurl,
            "startyear":startyear,
            "startmonth":startmonth,
            "endyear":endyear,
            "endmonth":endmonth})

class GroupPerformanceView(View):
    def get(self, request, group_id):
        if int(group_id) == 0:
            return HttpResponseRedirect('/performance/department_detail/')
        startyear = request.GET.get('startyear', '2018')
        startmonth = request.GET.get('startmonth', '1')
        endyear = request.GET.get('endyear', '2018')
        endmonth = request.GET.get('endmonth', '12')
        start = getMonthFirstDay(year=int(startyear), month=int(startmonth))
        end = getNextMonthFirstDay(year=int(endyear), month=int(endmonth))
        months = (int(endmonth) - int(startmonth)) + 1 + (int(endyear) - int(startyear)) * 12
        if months < 1:
            months = 1
        data = Task.objects.filter(group_id=group_id, project_status='finish')
        all_task = []
        gsp = 0
        for task in data:
            if task.project.end_time != None and task.project.end_time > start and task.project.end_time < end:
                all_task.append(task)
                gsp += task.getSP()
        gsp = round(gsp, 1)
        score = round(gsp/months, 1)
        if score > 100:
            score = 100
        kpiurl = reverse('performance:group_detail',kwargs={"group_id":group_id})
        return render(request, 'kpi-detail-team.html', {
            'gsp':gsp,
            'all_task':all_task,
            'group':Group.objects.get(pk=group_id),
            'score':score,
            'url':kpiurl,
            "startyear":startyear,
            "startmonth":startmonth,
            "endyear":endyear,
            "endmonth":endmonth})

class UserPerformanceView(View):
    def get(self, request, user_id):
        startyear = request.GET.get('startyear', '2018')
        startmonth = request.GET.get('startmonth', '1')
        endyear = request.GET.get('endyear', '2018')
        endmonth = request.GET.get('endmonth', '12')
        start = getMonthFirstDay(year=int(startyear), month=int(startmonth))
        end = getNextMonthFirstDay(year=int(endyear), month=int(endmonth))
        months = (int(endmonth) - int(startmonth)) + 1 + (int(endyear) - int(startyear)) * 12
        if months < 1:
            months = 1
        person_tasks = PersonTask.objects.filter(user_id=user_id,task_project_status='finish')
        psp = 0
        data = []
        for person_task in person_tasks:
            if person_task.task.project.end_time > start and person_task.task.project.end_time < end:
                print(person_task.task.project.end_time)
                psp += person_task.getSP()
                data.append(person_task)
        psp = round(psp, 1)
        score = round(psp/months, 1)
        if score > 100:
            score = 100
        kpiurl = reverse('performance:user_detail',kwargs={"user_id":user_id})
        return render(request, 'kpi-detail-person.html', {
            'psp':psp,
            'person_tasks':data,
            'user':UserProfile.objects.get(id=user_id),
            'score':score,
            'url':kpiurl,
            "startyear":startyear,
            "startmonth":startmonth,
            "endyear":endyear,
            "endmonth":endmonth})

def getMonthFirstDay(year=2018, month=1):
    return date(year=int(year),month=int(month),day=1)

def getNextMonthFirstDay(year=2018, month=1):
    year = int(year)
    month = int(month)
    if month == 12:
        return date(year=year + 1, month=1, day=1) - timedelta(days=1)
    else:
        return date(year=year, month=month + 1, day=1) - timedelta(days=1)

# def getMonthLastDay(year=2018, month=3):
#     year = int(year)
#     month = int(month)
#     if month == 12:
#         return date(year=year + 1, month=1, day=1) - timedelta(days=1)
#     else:
#         return date(year=year, month=month + 1, day=1) - timedelta(days=1)