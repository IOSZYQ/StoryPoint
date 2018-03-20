from django.shortcuts import render
from django.views.generic.base import View
from datetime import datetime, timedelta,date
from django.http import HttpResponse,HttpResponseRedirect

import re

from users.models import UserProfile
from group.models import Group
from project.models import Project,Task,PersonTask
# Create your views here.

class PerformanceView(View):
    def get(self, request):
        start_year = 2012
        start_month = 1
        end_year = 2018
        end_month = 6
        start = getMonthFirstDay(year=start_year, month=start_month)
        end = getMonthLastDay(year=end_year, month=end_month)
        all_project = Project.objects.filter(end_time__range=[start, end])
        months = (int(end_month) - int(start_month)) + 1 + (int(end_year) - int(start_year))*12
        time = "{0}.{1}-{2}.{3}".format(start_year, start_month, end_year,end_month)
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
        return render(request, 'kpi-team.html', {"result": result, "time":time})

class UserListPerformanceView(View):
    def get(self, request):
        start_year = 2017
        start_month = 1
        end_year = 2018
        end_month = 6
        start = getMonthFirstDay(year=start_year, month=start_month)
        end = getMonthLastDay(year=end_year, month=end_month)
        all_project = Project.objects.filter(end_time__range=[start, end])
        months = (int(end_month) - int(start_month)) + 1 + (int(end_year) - int(start_year)) * 12
        time = "{0}.{1}-{2}.{3}".format(start_year, start_month, end_year, end_month)

        data = {}
        result = []
        for user in UserProfile.objects.all():
            data[str(user.id)] = 0
            result.append({"id":str(user.id), 'name':user.username, 'jx':0})
        for project in all_project:
            for task in project.project_task.all():
                for person_task in task.person_task.all():
                    data[str(person_task.user.id)] += person_task.getSP()
        for dic in result:
            jx = round(data[dic['id']]/months,1)
            if jx > 100:
                jx = 100
            dic['jx'] = jx

        result = sorted(result, key=lambda user: user["jx"])
        result.reverse()

        return render(request, 'kpi-person.html', {'result':result,'time':time})

class DepartmentPerformanceView(View):
    def get(self, request):
        start_year = 2012
        start_month = 1
        end_year = 2018
        end_month = 6
        start = getMonthFirstDay(year=start_year, month=start_month)
        end = getMonthLastDay(year=end_year, month=end_month)
        sp = 0
        all_project = Project.objects.filter(end_time__range=[start, end])
        for project in all_project:
            sp += project.getSP()
        return render(request, 'kpi-detail-department.html', {'sp':sp,'all_project':all_project})

class GroupPerformanceView(View):
    def get(self, request, group_id):
        if int(group_id) == 0:
            return HttpResponseRedirect('/performance/department_detail/')
        start_year = 2017
        start_month = 1
        end_year = 2018
        end_month = 6
        start = getMonthFirstDay(year=start_year, month=start_month)
        end = getMonthLastDay(year=end_year, month=end_month)
        data = Task.objects.filter(group_id=group_id)
        all_task = []
        gsp = 0
        for task in data:
            if task.project.end_time > start and task.project.end_time < end:
                all_task.append(task)
                gsp += task.getSP()
        return render(request, 'kpi-detail-team.html', {'gsp':gsp,'all_task':all_task, 'group':Group.objects.get(pk=group_id)})

class UserPerformanceView(View):
    def get(self, request, user_id):
        start_year = 2017
        start_month = 1
        end_year = 2018
        end_month = 6
        start = getMonthFirstDay(year=start_year, month=start_month)
        end = getMonthLastDay(year=end_year, month=end_month)
        all_project = Project.objects.filter(end_time__range=[start, end])
        months = (int(end_month) - int(start_month)) + 1 + (int(end_year) - int(start_year)) * 12
        person_tasks = PersonTask.objects.filter(user_id=user_id)
        sp = 0
        data = []
        for person_task in person_tasks:
            if person_task.task.project.end_time > start and person_task.task.project.end_time < end:
                print(person_task.task.project.end_time)
                sp += person_task.getSP()
                data.append(person_task)


        return render(request, 'kpi-detail-person.html', {'sp':sp, 'person_tasks':data,'user':UserProfile.objects.get(id=user_id)})

# def getMonthFirstDay(year_month=None):
#     if year_month:
#         year_month = year_month.split('-')
#         if len(year_month) == 2:
#             year = int(year_month[0])
#             month = int(year_month[1])
#             if year and month and month>0 and month<13:
#                 return date(year=year,month=month, day=1)
#     return date(year=2017,month=12,day=31)
#
# def getMonthLastDay(year_month=None):
#     if year_month:
#         year_month = year_month.split('-')
#         if len(year_month) == 2:
#             year = int(year_month[0])
#             month = int(year_month[1])
#             if year and month and month>0 and month<13:
#                 if month == 12:
#                     lastDay = date(year=year+1,month=1, day=1) - timedelta(days=1)
#                 else:
#                     lastDay = date(year=year,month=month+1, day=1) - timedelta(days=1)
#                 return lastDay
#     return datetime.date(year=2050,month=1,day=1)

def getMonthFirstDay(year=2018, month=1):
    return date(year=int(year),month=int(month),day=1)

def getMonthLastDay(year=2018, month=3):
    year = int(year)
    month = int(month)
    if month == 12:
        return date(year=year + 1, month=1, day=1) - timedelta(days=1)
    else:
        return date(year=year, month=month + 1, day=1) - timedelta(days=1)