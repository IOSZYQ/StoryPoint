from django.shortcuts import render
from django.views.generic.base import View
from datetime import datetime, timedelta,date
from django.http import HttpResponse

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
        data = {"-1" : 0}
        result = [{'id':'-1', 'jx':0, 'name':'产品研发部'}]
        for group in Group.objects.all():
            data['{0}'.format(group.id)] = 0
            result.append({'id':'{0}'.format(group.id), 'jx':0, 'name':group.name})
        for project in all_project:
            data["-1"] += project.getSP()
            for task in project.project_task.all():
                data['{0}'.format(task.group.id)] += task.getSP()
        for dic in result:
            jx = round((data[dic['id']]/months/5) if(dic['id'] == '-1') else (data[dic['id']]/months),1)
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
    def post(self, request):
        all_project = Project.objects.all()
        start_time = request.GET.get('start', '')
        end_time = request.GET.get('end', '')
        start_time = '2018-1'
        end_time = '2018-3'
        if start_time and end_time:
            start = getMonthFirstDay(start_time)
            end = getMonthLastDay(end_time)
            months = (end.month - start.month + 1) + (end.year - start.year) * 12
            all_project = all_project.filter(end_time__range=[start, end])
        projectInfo = []
        apartment_sp = 0
        for project in all_project:
            if project.executing > 0 and project.acceptance > 0:
                weight = project.weight
                time = project.getTimeProportion()
                executing = project.getAcceptanceBugProportion()
                release = project.getReleaseBugProportion()
                impression = project.impression
                groupResult = []
                apartment_sp += project.getSP()
                for task in project.project_task.all():
                    group_name = task.group.name
                    group_weight = task.group.getScore(time=time, acceptance=executing, release=release,
                                                       impression=impression)
                    group_sp = task.gsp * group_weight * weight
                    groupResult.append({"groupName": group_name, "groupSP": group_sp})
                projectInfo.append({"name": project.name,
                                    "time": "{0}-{1}".format(project.start_time, project.end_time),
                                    "sp": project.getSP(),
                                    "group": groupResult})
        score = 100 if apartment_sp / 500 / months > 1 else apartment_sp * 100 / 500 / months
        result = {"score": score,
                  "sp": apartment_sp,
                  "project": projectInfo}

        return render(request, 'performance.html', {})

class GroupPerformanceView(View):
    def post(self, request):
        all_project = Project.objects.all()
        group_id = request.GET.get('group', '')
        group_id = 2
        group = Group.objects.get(pk=group_id)
        if group != None:
            start_time = request.GET.get('start', '')
            end_time = request.GET.get('end', '')
            start_time = '2018-1'
            end_time = '2018-3'
            if start_time and end_time:
                start = getMonthFirstDay(start_time)
                end = getMonthLastDay(end_time)
                months = (end.month - start.month + 1) + (end.year - start.year) * 12
                all_project = all_project.filter(end_time__range=[start, end])
            groupInfo = []
            group_all_sp = 0
            for project in all_project:
                if project.executing > 0 and project.acceptance > 0:
                    weight = project.weight
                    time = project.getTimeProportion()
                    executing = project.getAcceptanceBugProportion()
                    release = project.getReleaseBugProportion()
                    impression = project.impression
                    groupResult = []
                    task = project.project_task.filter(group_id=group_id).last()
                    if task != None:
                        group_weight = group.getScore(time=time, acceptance=executing, release=release,
                                                      impression=impression)
                        group_sp = task.gsp * group_weight * weight
                        group_all_sp += group_sp
                        personInfo = []
                        for person_task in task.person_task.all():
                            person_task_sp = person_task.psp * group_weight * weight
                            tasksp = task.gsp * group_weight * weight
                            # 项目经理的可获得「项目SP值*5%」的个人SP值
                            if person_task.user.id == project.manager_id:
                                person_task_sp += project.getSP() * 0.05
                            # 小组领导可获得「小组任务SP值*10%」的个人SP值
                            if person_task.user.id == task.group.id:
                                person_task_sp += tasksp * 0.1
                            personInfo.append({"name": person_task.user.username,
                                               "psp": person_task_sp})
                        groupInfo.append({"name": project.name,
                                          "time": "{0}-{1}".format(project.start_time, project.end_time),
                                          "sp": group_sp,
                                          "user": personInfo})
            score = 100 if group_all_sp / months > 1 else group_all_sp / months * 100
            result = {"score": score,
                      "sp": group_all_sp,
                      "group": groupInfo}

        return render(request, 'performance.html', {})

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
        # person_task = PersonTask.objects.filter(user_id=user_id).filter(task.project.end_time__range=[start,end])



        # all_project = Project.objects.all()
        # user_id = request.GET.get('user', '')
        # user_id = 2
        # user = UserProfile.objects.get(pk=user_id)
        # if user != None:
        #     start_time = request.GET.get('start', '')
        #     end_time = request.GET.get('end', '')
        #     start_time = '2018-1'
        #     end_time = '2018-3'
        #     if start_time and end_time:
        #         start = getMonthFirstDay(start_time)
        #         end = getMonthLastDay(end_time)
        #         months = (end.month - start.month + 1) + (end.year - start.year) * 12
        #         all_project = all_project.filter(end_time__range=[start, end])
        #     userInfo = []
        #     user_all_sp = 0
        #     for project in all_project:
        #         if project.executing > 0 and project.acceptance > 0:
        #             all_task = project.project_task.all()
        #             for task in all_task:
        #                 person_task = task.person_task.filter(user_id=user_id).last()
        #                 if person_task != None:
        #                     weight = project.weight
        #                     time = project.getTimeProportion()
        #                     executing = project.getAcceptanceBugProportion()
        #                     release = project.getReleaseBugProportion()
        #                     impression = project.impression
        #                     group_weight = task.group.getScore(time=time, acceptance=executing, release=release,
        #                                                        impression=impression)
        #                     person_task_sp = person_task.psp * group_weight * weight
        #                     tasksp = task.gsp * group_weight * weight
        #                     # 项目经理的可获得「项目SP值*5%」的个人SP值
        #                     if person_task.user.id == project.manager_id:
        #                         person_task_sp += project.getSP() * 0.05
        #                     # 小组领导可获得「小组任务SP值*10%」的个人SP值
        #                     if person_task.user.id == task.group.id:
        #                         person_task_sp += tasksp * 0.1
        #                     user_all_sp += person_task_sp
        #                     userInfo.append({"project": project.name,
        #                                      "time": "{0}-{1}".format(project.start_time, project.end_time),
        #                                      "name": person_task.user.username,
        #                                      "sp": person_task_sp})
        #     score = 100 if user_all_sp / months > 100 else user_all_sp / months / 100
        #     result = {"score": score,
        #               "sp": user_all_sp,
        #               "user": userInfo}

        return render(request, 'kpi-detail-person.html', {})

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
    return date(year=int(year),month=int(month),day=31)

def getMonthLastDay(year=2018, month=3):
    year = int(year)
    month = int(month)
    if month == 12:
        return date(year=year + 1, month=1, day=1) - timedelta(days=1)
    else:
        return date(year=year, month=month + 1, day=1) - timedelta(days=1)