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
        users = UserProfile.objects.all()
        return render(request, 'project.html', {
            "all_project":page_project,
            "all_managers":all_manager_names,
            "users":users,
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
            if Project.objects.filter(name=name):
                result = {"status": -1, 'msg': "该项目已经存在请更换项目名字"}
                return HttpResponse(dumps(result), content_type='application/json')
            start_time = request.POST.get("start_time", "")
            end_time = request.POST.get("end_time", "")
            manager = request.POST.get("manager", "")
            status = request.POST.get("status", "")
            project_id = request.POST.get("project_id", "")
            if project_id != '0':
                project = Project.objects.get(pk=project_id)
                project.manager = UserProfile.objects.get(pk=manager)
                if project == None:
                    result = {"status": -1, 'msg': "id错误"}
                    return HttpResponse(dumps(result), content_type='application/json')
            else:
                project = Project.objects.create(name=name, manager_id=manager)
            project.name = name
            if start_time != '':
                project.start_time = start_time
            if end_time != '':
                project.end_time = end_time
            project.status = status
            project.save()
            result = {"status":0}
            return HttpResponse(dumps(result), content_type='application/json')
        else:
            result = {"status":-1,'msg':'请填写名字'}
            return HttpResponse(dumps(result), content_type='application/json')

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
        project_id = request.POST.get("id", "")
        if project_id != '':
            project = Project.objects.get(pk=project_id)
            if project != None:
                for task in project.project_task.all():
                    for person_task in task.person_task.all():
                        person_task.delete()
                    task.delete()
                project.delete()
                result = {"status": 0}
                return HttpResponse(dumps(result), content_type='application/json')
        result = {"status": -1,'msg':'删除项目出错'}
        return HttpResponse(dumps(result), content_type='application/json')

class ProjectDetailView(View):
    def get(self, request, project_id):
        project = Project.objects.filter(id=project_id).last()
        if project == None:
            return HttpResponseRedirect('/')
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
            joined = request.POST.get("joined", "")
            task_id = request.POST.get("task_id", "")
            task = Task.objects.get(pk=task_id)
            task.gsp = gsp
            for id,psp in joined:
                task.person_task.add(PersonTask.objects.create(psp=psp,user_id=id,status=task.status,task_id=task_id))
            task.save()
            return HttpResponse(dumps({'status':0}), content_type='application/json')
        else:
            return HttpResponse(dumps({'status':-1, 'msg':{0}}).format(task_form.errors),
                                content_type='application/json')

class deleteTaskView(View):
    def post(self, request):
        task_id = request.POST.get("task_id", "")
        task = Task.objects.get(pk=task_id)
        if task != None:
            task.delete()
        return HttpResponse("{'status':'success}")

class getTask(View):
    def get(self, request,task_id):
        task = Task.objects.get(pk=task_id)
        return HttpResponse(dumps({task.getDic()}),content_type='application/json')