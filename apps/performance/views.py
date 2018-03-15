from django.shortcuts import render
from django.views.generic.base import View
from datetime import datetime, timedelta,date
from django.http import HttpResponse

import re

from users.models import UserProfile
from group.models import Group
from project.models import Project,Task
# Create your views here.

class PerformanceView(View):
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
        result = [{"id": 0, "name": "产品研发部", "jx": 0, "time": "{0}-{1}".format(start_time, end_time)}]
        for group in Group.objects.all():
            result.append({"id": group.id, "name": group.name, "jx": 0, "time": "{0}-{1}".format(start_time, end_time)})
        for project in all_project:
            if project.executing > 0 and project.acceptance > 0:
                weight = project.weight
                time = project.getTimeProportion()
                acceptance = project.getAcceptanceBugProportion()
                release = project.getReleaseBugProportion()
                impression = project.impression

                for dic in result:
                    group_name = dic["name"]
                    group_id = dic["id"]
                    if group_name == "产品研发部":
                        bm = time * 0.4 + acceptance * 0 + release * 0.3 + impression * 0.3
                        bmsp = 100 * project.sp * bm * weight / 500 / months
                        dic["jx"] = dic["jx"] + bmsp
                    task = project.project_task.filter(group__id=group_id).last()
                    if task != None:
                        gsp = task.gsp
                        group = Group.objects.get(pk=dic["id"])
                        dic["jx"] = dic["jx"] + group.getSp(time=time, acceptance=acceptance,release=release,impression=impression,gsp=gsp,months=months)

        return render(request, 'performance.html', {"result":result})

class UserListPerformanceView(View):
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
        result = []
        for user in UserProfile.objects.all():
            leader_id = 0
            # 判断是不是小组长,如果是获取小组的id
            if user.group_leader.all().last() != None:
                leader_id = user.group_leader.all().last().id
            print(user.group_leader.all())
            result.append({"id": user.id, "leader": leader_id, "name": user.username, "jx": 0,
                           "time": "{0}-{1}".format(start_time, end_time)})
        for project in all_project:
            if project.executing > 0 and project.acceptance > 0:
                weight = project.weight
                time = project.getTimeProportion()
                executing = project.getAcceptanceBugProportion()
                release = project.getReleaseBugProportion()
                impression = project.impression

                for dic in result:
                    user_id = dic["id"]
                    leader_id = dic["leader"]
                    for task in project.project_task.all():
                        for person_task in task.person_task.filter(user_id=user_id):
                            group_weight = task.group.getScore(time=time, acceptance=executing, release=release,
                                                               impression=impression)
                            person_task_sp = person_task.psp * group_weight * weight
                            tasksp = task.gsp * group_weight * weight
                            # 项目经理的可获得「项目SP值*5%」的个人SP值
                            if user_id == project.manager_id:
                                person_task_sp += project.getSP() * 0.05
                            # 小组领导可获得「小组任务SP值*10%」的个人SP值
                            if leader_id == task.group.id:
                                person_task_sp += tasksp * 0.1
                            dic["jx"] = dic["jx"] + person_task_sp
        for dic in result:
            jx = dic['jx'] / months
            dic['jx'] = 100 if jx > 100 else jx
        result = sorted(result, key=lambda user: user["jx"])
        result.reverse()

        return render(request, 'performance.html', {})

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
        start = request.POST.get('start', '')
        end = request.POST.get('end', '')
        all_project = Project.objects.filter(end_time__in=[start, end])

        return render(request, 'performance.html', {})

class UserPerformanceView(View):
    def post(self, request):
        start = request.POST.get('start', '')
        end = request.POST.get('end', '')
        all_project = Project.objects.filter(end_time__in=[start, end])

        return render(request, 'performance.html', {})

def getMonthFirstDay(year_month=None):
    if year_month:
        year_month = year_month.split('-')
        if len(year_month) == 2:
            year = int(year_month[0])
            month = int(year_month[1])
            if year and month and month>0 and month<13:
                return date(year=year,month=month, day=1)
    return date(year=2017,month=12,day=31)

def getMonthLastDay(year_month=None):
    if year_month:
        year_month = year_month.split('-')
        if len(year_month) == 2:
            year = int(year_month[0])
            month = int(year_month[1])
            if year and month and month>0 and month<13:
                if month == 12:
                    lastDay = date(year=year+1,month=1, day=1) - timedelta(days=1)
                else:
                    lastDay = date(year=year,month=month+1, day=1) - timedelta(days=1)
                return lastDay
    return datetime.date(year=2050,month=1,day=1)


# def getMonthFirstDayAndLastDay(year=None, month=None):
#     """
#     :param year: 年份，默认是本年，可传int或str类型
#     :param month: 月份，默认是本月，可传int或str类型
#     :return: firstDay: 当月的第一天，datetime.date类型
#               lastDay: 当月的最后一天，datetime.date类型
#     """
#     if year:
#         year = int(year)
#     else:
#         year = datetime.date.today().year
#
#     if month:
#         month = int(month)
#     else:
#         month = datetime.date.today().month
#
#     # 获取当月第一天的星期和当月的总天数
#     firstDayWeekDay, monthRange = calendar.monthrange(year, month)
#
#     # 获取当月的第一天
#     firstDay = datetime.date(year=year, month=month, day=1)
#     lastDay = datetime.date(year=year, month=month, day=monthRange)
#
#     return firstDay, lastDay

