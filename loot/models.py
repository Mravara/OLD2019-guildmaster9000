from django.conf import settings
from django.db import models
from datetime import datetime
from items.models import Item
from raid.models import Raid


class Loot(models.Model):
    character = models.ForeignKey('members.Character', on_delete=models.PROTECT, null=True)
    raid = models.ForeignKey('raid.Raid', on_delete=models.PROTECT, null=True)
    item = models.ForeignKey('items.Item', on_delete=models.PROTECT)
    item_info = models.ForeignKey('items.ItemInfo', on_delete=models.PROTECT, null=True)
    price_percentage = models.FloatField(null=True, default=100)
    given_by = models.ForeignKey('members.Member', on_delete=models.PROTECT, related_name='given_by', null=True)
    timestamp = models.DateTimeField(default=datetime.now)
    comment = models.CharField(default='', max_length=256)

    @property
    def gp(self):
        return (((self.item.get_item_value**2) * 0.04 * self.item_info.slot_value) * self.raid.dungeon.gp_modifier) * (self.price_percentage / 100)

