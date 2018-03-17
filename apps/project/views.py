from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from json import dumps

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from .forms import *
from performance.views import getMonthFirstDay,getMonthLastDay
class ProjectListView(View):
    def get(self, request):
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
    def post(self,request):
        manager_name = request.POST.get('manager','')
        start = getMonthFirstDay(year=request.POST.get('startyear',''), month=request.POST.get('startmonth',''))
        end = getMonthLastDay(year=request.POST.get('endyear',''), month=request.POST.get('endmonth',''))
        all_project = Project.objects.filter(end_time__range=[start, end])
        if manager_name != '全部':
            all_project = all_project.filter(manager__username=manager_name)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_project, 10, request=request)
        page_project = p.page(page)

        all_manager_names = set(Project.objects.values_list('manager__username', flat=True))
        return render(request, 'project.html', {
            "all_project": page_project,
            "all_managers": all_manager_names,
            "start_time": start,
            "end_time": end,
            "manager": manager_name
        })

class CreateEditProjectInfoView(View):
    """
    管理员用户添加或者编辑项目信息
    """
    def post(self, request):
        project_form = CreateEditProjectForm(request.POST)
        if project_form.is_valid():
            name = request.POST.get("name", "")
            start_time = request.POST.get("start_time", "")
            end_time = request.POST.get("end_time", "")
            manager = request.POST.get("manager", "")
            status = request.POST.get("status", "")
            project_id = request.POST.get("project_id", "")
            project = Project.objects.get(pk=project_id)
            if project == None:
                project = Project()
            status = project.getStatusName(str=status)
            project.name = name
            project.start_time = start_time.replace('年','-').replace('月','-').replace('日','')
            project.end_time = end_time.replace('年','-').replace('月','-').replace('日','')
            project.manager = UserProfile.objects.get(pk=manager)
            project.status = status
            project.save()
            # return HttpResponseRedirect("www.baidu.com")
            # return HttpResponseRedirect('/project/detail/{0}/'.format(project_id))
            result = {"status":0, 'msg':"成功了"}
            return HttpResponse(dumps(result), content_type='application/json')
        else:
            result = {"status":'-1'}
            return HttpResponse(dumps(result).format(project_form.errors), content_type='application/json')

class EditorProjectDetailView(View):
    def post(self, request):
        project_form = ProjectInfoForm(request.POST)
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
            result = {"status":'0'}
            return HttpResponse(dumps(result), content_type='application/json')
        else:
            result = {"status":'-1',"msg":'信息格式不正确'}
            return HttpResponse(dumps(result).format(project_form.errors),content_type='application/json')

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
            tasks = Task.objects.filter(project__id = project.id)
            info = []
            info.append({"key":"产品研发部的项目评分={0}".format(project.getScore()),"value":"项目评分=消耗时间比*40% + 发布缺陷比*30% + 项目成效*30%"})
            info.append({"key":"产品研发部的项目SP值={0}".format(project.getSP()),"value":"项目SP值=项目标准SP值*权重*「部门／小组／个人」项目评分"})
            users = UserProfile.objects.order_by('id')
            groups = Group.objects.order_by('id')
            if project:
                return render(request, 'project-detail.html', {
                    "project":project,
                    'tasks':tasks,
                    "users":users,
                    'groups':groups
                })

class CreateEditTaskInfoView(View):
    def post(self,request):
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            projectId = request.POST.get("projectId","")
            status = request.POST.get("status", "")
            group = request.POST.get("group", "")
            description = request.POST.get("description", "")
            task_id = request.POST.get("task_id", "")
            if task_id != "":
                task = Task.objects.get(pk=task_id)
            if task_id == "" or task== None:
                task = Task.objects.create(project_id=projectId,group_id=group)
            task.status = status
            task.description = description
            task.save()
            result = {'status':0}
            return HttpResponse(dumps(result), content_type='application/json')
        else:
            result = {'status':-1, 'msg':"{0}".format(task_form.errors)}
            return HttpResponse(dumps(result),
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