from django.db import models

# Create your models here.
from users.models import UserProfile

class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name="组名")
    members = models.ManyToManyField(UserProfile, related_name="user_groups", verbose_name="小组成员", null=True, blank=True)
    leader = models.ForeignKey(UserProfile, related_name="group_leader", verbose_name="小组组长", null=True, blank=True)
    timeProportion = models.FloatField(default=0.4, verbose_name="消耗时间比")
    acceptanceBugProportion = models.FloatField(default=0, verbose_name="验收缺陷比")
    releaseBugProportion = models.FloatField(default=0.3, verbose_name="发布缺陷比")
    impressionProportion = models.FloatField(default=0.3, verbose_name="项目成效")

    class Meta:
        verbose_name = "小组"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def getScore(self, time=1, acceptance=1, release=1, impression=1):
        return round(time*self.timeProportion + acceptance*self.acceptanceBugProportion + release*self.releaseBugProportion + impression*self.impressionProportion,2)

    def getSp(self, time=1, acceptance=1, release=1, impression=1, gsp=0, months=3):
        return int(self.getScore(time=time,acceptance=acceptance,impression=impression)*gsp/months)