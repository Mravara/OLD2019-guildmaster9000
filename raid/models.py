from django.conf import settings
from django.db import models
from datetime import datetime


class Raid(models.Model):

    class State(models.IntegerChoices):
        IN_PROGRESS = 0
        PAUSED = 1
        FAILED = 2
        SUCCESS = 3

    dungeon = models.ForeignKey('dungeons.Dungeon', on_delete=models.PROTECT)
    leader = models.ForeignKey('members.Member', related_name='leader', on_delete=models.PROTECT)
    state = models.IntegerField(choices=State.choices, default=State.IN_PROGRESS)
    start = models.DateTimeField(default=datetime.now)
    end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{}: {}".format(self.start, self.dungeon.name)

    @property
    def done(self):
        return self.end is not None



class RaidCharacter(models.Model):
    raid = models.ForeignKey('raid.Raid', related_name='raidcharacter', on_delete=models.CASCADE)
    character = models.ForeignKey('members.Character', on_delete=models.CASCADE, null=True)
    start = models.DateTimeField(default=datetime.now)
    end = models.DateTimeField(null=True, blank=True)
    closed = models.BooleanField(default=False)
    earned_ep = models.FloatField(default=0)

    def __str__(self):
        return self.character.name

    @property
    def done(self):
        return self.end is not None
    
    @property
    def closed_raid(self):
        return self.closed



class BenchedRaidCharacter(models.Model):
    raid = models.ForeignKey('raid.Raid', related_name='benchedraidcharacter', on_delete=models.CASCADE)
    character = models.ForeignKey('members.Character', on_delete=models.CASCADE, null=True)
    start = models.DateTimeField(default=datetime.now)
    end = models.DateTimeField(null=True, blank=True)
    ticks = models.IntegerField(default=0)
    closed = models.BooleanField(default=False)
    earned_ep = models.FloatField(default=0)

    def __str__(self):
        return self.character.name

    @property
    def waiting(self):
        return self.end is None

    @property
    def closed_raid(self):
        return self.closed
