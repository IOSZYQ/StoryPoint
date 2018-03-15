from django.db import models

# Create your models here.
from users.models import UserProfile

class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name="组名")
    members = models.ManyToManyField(UserProfile, related_name="user_groups", verbose_name="小组成员", null=True, blank=True)
    leader = models.ForeignKey(UserProfile, related_name="group_leader", verbose_name="小组组长", null=True, blank=True)
    class Meta:
        verbose_name = "小组"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def getScore(self, time=1, acceptance=1, release=1, impression=1):
        if self.name == "产品研发部":
            return time*0.4 + acceptance*0 + release*0.3 + impression*0.3
        if self.name == "产品组":
            return time*0.3 + acceptance*0 + release*0.2 + impression*0.5
        if self.name == "设计组":
            return time*0.4 + acceptance*0 + release*0.2 + impression*0.4
        if self.name == "技术组":
            return time*0.5 + acceptance*0 + release*0.3 + impression*0.2
        if self.name == "测试组":
            return time*0.3 + acceptance*0 + release*0.4 + impression*0.3
        return 0

    def getSp(self, time=1, acceptance=1, release=1, impression=1, gsp=0, months=3):
        return self.getScore(time=time,acceptance=acceptance,impression=impression)*gsp/months