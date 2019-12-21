from django.conf import settings
from django.db import models



class Member(models.Model):

    class Rank(models.IntegerChoices):
        MEMBER = 0,
        RAID_LEADER = 10
        OFFICER = 100
        ADMIN = 1000

    discord_id = models.BigIntegerField(null=True)
    name = models.CharField(max_length=50)
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Dungeon(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name



class Raid(models.Model):
    dungeon = models.ForeignKey('Dungeon', on_delete=models.PROTECT)
    leader = models.ForeignKey('Member', on_delete=models.PROTECT)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(default=None)

    def __str__(self):
        return "{}: {}".format(self.start, self.dungeon.name)



class RaidMember(models.Model):
    member = models.ForeignKey('Member', on_delete=models.PROTECT)
    raid = models.ForeignKey('Raid', on_delete=models.PROTECT)
    name = models.CharField(max_length=64)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(default=None)

    def __str__(self):
        return self.member.name



class BenchedRaidMember(models.Model):
    member = models.ForeignKey('Member', on_delete=models.PROTECT)
    raid = models.ForeignKey('Raid', on_delete=models.PROTECT)
    name = models.CharField(max_length=64)
    ticks = models.IntegerField()
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(default=None)

    def __str__(self):
        return self.member.name



class Loot(models.Model):
    member = models.ForeignKey('Member', on_delete=models.PROTECT)
    raid = models.ForeignKey('Raid', on_delete=models.PROTECT)
    item = models.ForeignKey('Item', on_delete=models.PROTECT)
    value = models.FloatField()
    cost = models.IntegerField()
    given_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    timestamp = models.DateTimeField(auto_now_add=True)



class Item(models.Model):

    class Quality(models.IntegerChoices):
        POOR = 0,
        COMMON = 1
        UNCOMMON = 2
        RARE = 3
        EPIC = 4
        LEGENDARY = 5


    wow_id = models.IntegerField(default=0)
    name = models.CharField(max_length=128)
    level = models.IntegerField
    quality = models.IntegerField(choices=Quality.choices)
    ep = models.IntegerField()

    def __str__(self):
        return self.name
