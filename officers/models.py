from django.conf import settings
from django.db import models
from datetime import datetime

class Log(models.Model):

    class Action(models.IntegerChoices):
        NEW_MEMBER = 0
        GIVE_LOOT = 1
        GIVE_EP = 2
        CREATE_RAID = 3
        END_RAID = 4
        ADD_TO_RAID = 5
        REMOVE_FROM_RAID = 6
        DECAY = 7
        UNLOCK_RAID = 8
        DELETE_LOOT = 9
        BENCH = 10
        UNBENCH = 11

    writer = models.ForeignKey('members.Member', related_name='writer', on_delete=models.PROTECT)
    target = models.ForeignKey('members.Character', related_name='target',  on_delete=models.PROTECT, null=True, blank=True)
    target_member = models.ForeignKey('members.Member', related_name='target_member',  on_delete=models.PROTECT, null=True, blank=True)
    action = models.IntegerField(choices=Action.choices)
    raid = models.ForeignKey('raid.Raid', related_name='raid', on_delete=models.PROTECT, null=True, blank=True)
    item = models.ForeignKey('items.Item', related_name='item', on_delete=models.PROTECT, null=True, blank=True)
    value = models.CharField(max_length=128, blank=True, null=True)
    timestamp = models.DateTimeField(default=datetime.now)

    @property
    def string_action(self):
        if self.action == 0:
            return 'New Member'
        elif self.action == 1:
            return 'Give Loot'
        elif self.action == 2:
            return 'Give EP'
        elif self.action == 3:
            return 'Create Raid'
        elif self.action == 4:
            return 'End Raid'
        elif self.action == 5:
            return 'Add To Raid'
        elif self.action == 6:
            return 'Remove From Raid'
        elif self.action == 7:
            return 'Decay'
        elif self.action == 8:
            return 'Unlock Raid'
        elif self.action == 9:
            return 'Delete Loot'
        elif self.action == 10:
            return 'Bench'
        elif self.action == 11:
            return 'Unbench'
        
