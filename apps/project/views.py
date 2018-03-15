from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import render_to_response

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from .forms import *
from performance.views import getMonthFirstDay,getMonthLastDay
class ProjectListView(View):
    def get(self, request):
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
                months = (end.month - start.month + 1)+(end.year-start.year)*12
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
                                personInfo.append({"name":person_task.user.name,
                                                   "psp":person_task_sp})
                        groupInfo.append({"name":project.name,
                                          "time": "{0}-{1}".format(project.start_time, project.end_time),
                                          "sp":group_sp,
                                          "user":personInfo})
            score = 100 if group_all_sp/months > 1 else group_all_sp/months*100
            result = {"score": score,
                      "sp": group_all_sp,
                      "group": groupInfo}

        all_project = Project.objects.all()
        start_time = request.GET.get('start', '')
        end_time = request.GET.get('end', '')
        if start_time and end_time :
            start = getMonthFirstDay(start_time)
            end = getMonthLastDay(end_time)
            all_project = all_project.filter(end_time__range=[start, end])

        manager_name = request.GET.get('manager', '')
        if manager_name:
            all_project.filter(manager__username=manager_name)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_project, 10, request=request)
        page_project = p.page(page)

        all_manager_names = set(Project.objects.values_list('manager__username', flat=True))
        return render(request, 'project.html', {
            "all_project":page_project,
            "all_managers":all_manager_names,
        })

class CreateEditProjectInfoView(View):
    """
    管理员用户添加或者编辑项目信息
    """
    def post(self, request):
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            name = request.POST.get("name", "")
            start_time = request.POST.get("name", "")
            manager = request.POST.get("name", "")
            status = request.POST.get("name", "")

            project_id = request.POST.get("name", "")
            project = Project.objects.get(pk=project_id)
            if project == None:
                project = Project()
            project.name = name
            project.start_time = start_time
            project.manager = manager
            project.status = status
            project.save()
            return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail', 'msg':{0}}".format(project_form.errors), content_type='application/json')

class EditorProjectDetailView(View):
    def post(self, request):
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project_id = request.POST.get("project_id", "")
            project = Project.objects.get(pk=project_id)
            if project == None:
                return render(request, 'product-list.html', {"error": "项目不存在"})
            weight = request.POST.get("weight", "")
            sp = request.POST.get("sp", "")
            impression = request.POST.get("impression", "")
            executing = request.POST.get("executing", "")
            acceptance = request.POST.get("acceptance", "")
            acceptance_serious_bug = request.POST.get("acceptance_serious_bug", "")
            acceptance_medium_bug = request.POST.get("acceptance_medium_bug", "")
            acceptance_slight_bug = request.POST.get("acceptance_slight_bug", "")
            release_serious_bug = request.POST.get("release_serious_bug", "")
            release_medium_bug = request.POST.get("release_medium_bug", "")
            release_slight_bug = request.POST.get("release_slight_bug", "")

            project.weight = weight
            project.sp = sp
            project.impression = impression
            project.executing = executing
            project.acceptance = acceptance
            project.acceptance_serious_bug = acceptance_serious_bug
            project.acceptance_medium_bug = acceptance_medium_bug
            project.acceptance_slight_bug = acceptance_slight_bug
            project.release_serious_bug = release_serious_bug
            project.release_medium_bug = release_medium_bug
            project.release_slight_bug = release_slight_bug
            project.save()
            return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail', 'msg':{0}}".format(project_form.errors),content_type='application/json')

class deleteProjectView(View):
    def post(self, request):
        project_id = request.POST.get("project_id", "")
        project = Project.objects.get(pk=project_id)
        if project != None:
            project.delete()
        return HttpResponse("{'status':'success}")

class ProjectDetailView(View):
    def get(self, request, project_id):
            project = Project.objects.get(id=project_id)

            if project:
                return render(request, 'detail.html', {
                    "project":project
                })

class CreateEditTaskInfoView(View):
    def post(self,request):
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            status = request.POST.get("status", "")
            group = request.POST.get("group", "")
            description = request.POST.get("description", "")
            task_id = request.POST.get("task_id", "")
            task = Task.objects.get(pk=task_id)
            if task == None:
                task = Task()
            task.status = status
            task.group = group
            task.description = description
            task.save()
            return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail', 'msg':{0}}".format(task_form.errors),
                                content_type='application/json')


class EditTaskDetailView(View):
    def post(self, request):
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            gsp = request.POST.get("gsp", "")
            members = request.POST.get("members", "")
            task_id = request.POST.get("task_id", "")
            task = Task.objects.get(pk=task_id)
            task.gsp = gsp
            task.members.add(UserProfile.objects.get(pk=members))
            task.save()
            return HttpResponse("{'status':'success', 'msg':'123'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail', 'msg':{0}}".format(task_form.errors),
                                content_type='application/json')

class deleteTaskView(View):
    def post(self, request):
        task_id = request.POST.get("task_id", "")
        task = Task.objects.get(pk=task_id)
        if task != None:
            task.delete()
        return HttpResponse("{'status':'success}")