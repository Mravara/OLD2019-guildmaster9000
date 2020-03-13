from django.conf import settings
from django.db import models
from datetime import datetime

class Log(models.Model):

    class Action(models.IntegerChoices):
        NEW_MEMBER = 0
        GIVE_ITEM = 1
        GIVE_EP = 2
        CREATE_RAID = 3
        END_RAID = 4
        ADD_TO_RAID = 5
        REMOVE_FROM_RAID = 6
        DECAY = 7

    writer = models.ForeignKey('members.Member', related_name='writer', on_delete=models.PROTECT)
    target = models.ForeignKey('members.Member', related_name='target',  on_delete=models.PROTECT)
    action = models.IntegerField(choices=Action.choices)
    raid = models.ForeignKey('raid.Raid', related_name='raid', on_delete=models.PROTECT, null=True, blank=True)
    item = models.ForeignKey('items.Item', related_name='item', on_delete=models.PROTECT, null=True, blank=True)
    value = models.CharField(max_length=128)
    timestamp = models.DateTimeField(default=datetime.now)
