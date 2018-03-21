from django.db import models
from datetime import datetime
from json import dumps

from group.models import Group
from users.models import UserProfile
import users

# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name="项目名称")
    manager = models.ForeignKey(UserProfile, verbose_name="项目经理", related_name="manager_projects")
    create = models.DateField(auto_now_add=True, verbose_name="项目创建时间")
    start_time = models.DateField(auto_now_add=True,verbose_name="项目开始时间")
    end_time = models.DateField(auto_now_add=True,verbose_name="实际终止时间")
    expect_end_time = models.DateField(auto_now_add=True,verbose_name="预计终止时间")
    executing = models.IntegerField(default=0, verbose_name="项目执行时间")
    acceptance = models.IntegerField(default=0,verbose_name="项目验收时间")
    sp = models.IntegerField(verbose_name="项目SP值", default=0)
    weight = models.FloatField(default=1.0, verbose_name="项目权重")
    impression = models.FloatField(verbose_name="项目成效", default=0)
    acceptance_serious_bug = models.IntegerField(default=0, verbose_name="验收阶段严重缺陷")
    acceptance_medium_bug = models.IntegerField(default=0, verbose_name="验收阶段中级缺陷")
    acceptance_slight_bug = models.IntegerField(default=0, verbose_name="验收阶段低级缺陷")
    release_serious_bug = models.IntegerField(default=0, verbose_name="发布阶段严重缺陷")
    release_medium_bug = models.IntegerField(default=0, verbose_name="发布阶段中级缺陷")
    release_slight_bug = models.IntegerField(default=0, verbose_name="发布阶段低级缺陷")
    status = models.CharField(choices=(("executing","执行"),("acceptance","验收"),("release","发布"),("suspend","滞后")),default="executing",max_length=15)

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def getStatusName(self, str='执行'):
        if str == '执行':
            return 'executing'
        if str == '验收':
            return 'acceptance'
        if str == '发布':
            return 'release'
        return 'executing'

    def getTimeProportion(self):
        if self.executing > 0 and self.acceptance > 0:
            time = self.sp/22.0/(self.executing+self.acceptance)
            if time > 0 and time < 1:
                return round(time,2)
        return 1

    def getAcceptanceBugProportion(self):
        if self.acceptance_serious_bug > 0 or self.acceptance_slight_bug > 0 or self.acceptance_slight_bug > 0:
            acceptance = self.sp*1.0/(15*self.acceptance_serious_bug + 5*self.acceptance_medium_bug + 2*self.acceptance_slight_bug)
            if acceptance > 0 and acceptance < 1:
                return round(acceptance,2)
        return 1

    def getReleaseBugProportion(self):
        if self.release_serious_bug > 0 or self.release_medium_bug > 0 or self.release_slight_bug > 0:
            release =self.sp*1.0/(1500*self.release_serious_bug + 500*self.release_medium_bug + 200*self.release_slight_bug)
            if release > 0 and release < 1:
                return round(release,2)
        return 1

    def getScore(self):
        return round(self.getTimeProportion()*0.4 + self.getReleaseBugProportion()*0.3 + self.impression*0.3, 3)

    def getSP(self):
        return self.sp*self.weight*self.getScore()


class Task(models.Model):
    project = models.ForeignKey(Project, verbose_name="项目", related_name="project_task")
    group = models.ForeignKey(Group, verbose_name="任务参与团队",null=True,blank=True, related_name="group_task")
    # members = models.ManyToManyField(UserProfile, verbose_name="任务参与人员", null=True, blank=True, related_name="tasks")

    status = models.CharField(choices=(("executing","执行"),("acceptance","验收"),("release","发布")),default="executing",max_length=15)
    description = models.CharField(max_length=1000, null=True, blank=True)
    gsp = models.IntegerField(verbose_name="小组SP值", default=0)
    create = models.DateField(auto_now_add=True, verbose_name="任务创建时间")
    status = models.CharField(choices=(("executing","执行"),("acceptance","验收"),("release","发布"),("suspend","滞后")),default="executing",max_length=15)

    class Meta:
        verbose_name = "小组任务"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.description

    def getDic(self):
        members = []
        for user in self.group.members.all():
            userId = user.id
            username= user.username
            psp = 0
            contain = False
            person_task = PersonTask.objects.filter(user_id = userId,task_id=self.id).last()
            if person_task != None:
                psp = person_task.psp
                contain = True
            members.append({'userid':userId,'username':username,'psp': psp,'contain':contain})
        return {'id':self.id, 'gsp':self.gsp,'members':members,'groupname':self.group.name, 'status':self.status}

    def getScore(self):
        return round(self.project.getTimeProportion()*self.group.timeProportion +
                     self.project.getAcceptanceBugProportion()*self.group.acceptanceBugProportion +
                     self.project.getReleaseBugProportion()*self.group.releaseBugProportion +
                     self.project.impression*self.group.impressionProportion, 2)

    def getSP(self):
        return round(self.gsp*self.project.weight*self.getScore(),1)

    def scoreDescription(self):
        return "{0}项目评分=消耗时间比({1})*{2}% + 发布缺陷比({3})*{4}% + 项目成效({5})*{6}%".format(self.group.name,self.project.getTimeProportion(),int(self.group.timeProportion*100), self.project.getReleaseBugProportion(), int(self.group.releaseBugProportion*100),self.project.impression, int(self.group.impressionProportion*100))

    def spDescription(self):
        return  "{0}项目SP值=小组标准GSP值({1})*权重({2})*{3}项目评分({4})".format(self.group.name,self.gsp, self.project.weight,self.group.name, self.getScore())

class PersonTask(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="任务完成人", null=True, blank=True, related_name="task_user")
    psp = models.IntegerField(verbose_name="个人sp值", default=0)
    task = models.ForeignKey(Task, verbose_name="小组任务", null=True, blank=True, related_name="person_task")
    create = models.DateField(auto_now_add=True, verbose_name="任务创建时间")
    status = models.CharField(choices=(("executing","执行"),("acceptance","验收"),("release","发布"),("suspend","滞后")),default="executing",max_length=15)

    class Meta:
        verbose_name = "个人任务"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username

    def getScore(self):
        return round(self.task.project.getTimeProportion()*self.task.group.timeProportion +
                     self.task.project.getAcceptanceBugProportion()*self.task.group.acceptanceBugProportion +
                     self.task.project.getReleaseBugProportion()*self.task.group.releaseBugProportion +
                     self.task.project.impression*self.task.group.impressionProportion, 3)

    def getSP(self):
        sp = self.psp*self.task.project.weight*self.getScore()
        if self.user.id == self.task.group.leader.id :
            sp += self.task.getSP()*0.1
        if self.user.id == self.task.project.manager.id:
            sp += self.task.project.getSP()*0.05
        return round(sp,1)

