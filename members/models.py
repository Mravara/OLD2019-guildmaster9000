from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from loot.models import Loot
from django.db.models import F


class Member(models.Model):

    class Rank(models.IntegerChoices):
        MEMBER = 0
        RAIDER = 5
        RAID_LEADER = 10
        OFFICER = 100
        ADMIN = 1000

    class MemberClass(models.IntegerChoices):
        DRUID = 0
        HUNTER = 1
        MAGE = 2
        PRIEST = 3
        ROGUE = 4
        SHAMAN = 5
        WARLOCK = 6
        WARRIOR = 7

    user = models.OneToOneField(User, related_name='member', on_delete=models.CASCADE, blank=True, null=True)
    discord_id = models.BigIntegerField(null=True)
    name = models.CharField(max_length=64)
    member_class = models.IntegerField(choices=MemberClass.choices, null=True)
    rank = models.IntegerField(choices=Rank.choices, default=Rank.MEMBER, null=True)
    joined = models.DateTimeField(default=timezone.now)
    ep = models.IntegerField(default=0)
    gp = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @staticmethod
    def get_member(request):
        return request.user.member

    @property
    def priority(self):
        return self.ep / max(self.gp, 1)

    @property
    def is_officer(self):
        return self.rank >= Member.Rank.OFFICER

    @property
    def loot_gp(self):
        gp = 0
        loot = Loot.objects.filter(member=self)
        for l in loot:
            gp += l.gp
        return gp

    @property
    def class_color(self):
        if self.member_class == Member.MemberClass.DRUID:
            return "#FF7D0A60"
        elif self.member_class == Member.MemberClass.HUNTER:
            return "#A9D27160"
        elif self.member_class == Member.MemberClass.MAGE:
            return "#40C7EB60"
        elif self.member_class == Member.MemberClass.PRIEST:
            return "#FFFFFF60"
        elif self.member_class == Member.MemberClass.ROGUE:
            return "#FFF56960"
        elif self.member_class == Member.MemberClass.SHAMAN:
            return "#0070DE60"
        elif self.member_class == Member.MemberClass.WARLOCK:
            return "#8787ED60"
        elif self.member_class == Member.MemberClass.WARRIOR:
            return "#C79C6E60"
        else:
            return "#FFFFFF"


class Character(models.Model):
    name = models.CharField(max_length=64)
    member = models.ForeignKey('members.Member', on_delete=models.CASCADE)


class Decay(models.Model):
    member = models.ForeignKey('members.Member', on_delete=models.PROTECT)
    percentage = models.FloatField()
    time = models.DateTimeField(default=timezone.now)
