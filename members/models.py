from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from loot.models import Loot
from django.db.models import F


class Member(models.Model):

    class Rank(models.IntegerChoices):
        MEMBER = 0
        RAID_LEADER = 10
        OFFICER = 100
        ADMIN = 1000

    class MemberClass(models.IntegerChoices):
        DRUID = 0
        HUNTER = 1
        MAGE = 2
        Priest = 3
        ROGUE = 4
        SHAMAN = 5
        WARLOCK = 6
        WARRIOR = 7

    user = models.OneToOneField(User, related_name='member', on_delete=models.CASCADE, blank=True, null=True)
    discord_id = models.BigIntegerField(null=True)
    name = models.CharField(max_length=50)
    member_class = models.IntegerField(choices=MemberClass.choices, null=True)
    rank = models.IntegerField(choices=Rank.choices, default=Rank.MEMBER, null=True)
    joined = models.DateTimeField(auto_now_add=True, null=True)
    ep = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @staticmethod
    def get_member(request):
        return Member.objects.get(user=request.user)

    @property
    def priority(self):
        return self.ep / max(self.gp, 1)

    @property
    def is_officer(self):
        return self.rank >= Member.Rank.OFFICER

    @property
    def gp(self):
        gp = 0
        loot = Loot.objects.filter(member=self)
        for l in loot:
            gp += l.gp
        return gp

