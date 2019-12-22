from django.conf import settings
from django.db import models
from members.models import Member
from items.models import Item
from dungeons.models import Dungeon



class Raid(models.Model):

    class State(models.IntegerChoices):
        IN_PROGRESS = 0
        PAUSED = 1
        FAILED = 2
        SUCCESS = 3

    dungeon = models.ForeignKey('dungeons.Dungeon', on_delete=models.PROTECT)
    leader = models.ForeignKey('members.Member', on_delete=models.PROTECT)
    state = models.IntegerField(choices=State.choices, default=State.IN_PROGRESS)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{}: {}".format(self.start, self.dungeon.name)



class RaidMember(models.Model):
    member = models.ForeignKey('members.Member', on_delete=models.PROTECT)
    raid = models.ForeignKey('Raid', on_delete=models.PROTECT)
    name = models.CharField(max_length=64)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.member.name



class BenchedRaidMember(models.Model):
    member = models.ForeignKey('members.Member', on_delete=models.PROTECT)
    raid = models.ForeignKey('Raid', on_delete=models.PROTECT)
    name = models.CharField(max_length=64)
    ticks = models.IntegerField()
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.member.name


