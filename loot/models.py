from django.conf import settings
from django.db import models
from datetime import datetime
from items.models import Item
from raid.models import Raid


class Loot(models.Model):
    member = models.ForeignKey('members.Member', on_delete=models.PROTECT)
    raid = models.ForeignKey('raid.Raid', on_delete=models.PROTECT, null=True)
    item = models.ForeignKey('items.Item', on_delete=models.PROTECT)
    item_info = models.ForeignKey('items.ItemInfo', on_delete=models.PROTECT, null=True)
    price_percentage = models.FloatField(null=True, default=100)
    given_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    timestamp = models.DateTimeField(default=datetime.now)

    @property
    def gp(self):
        return ((self.item.get_item_value**2) * 0.04 * self.item_info.slot_value) * (self.price_percentage / 100)

