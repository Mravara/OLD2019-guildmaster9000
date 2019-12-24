from django.conf import settings
from django.db import models
from members.models import Member
from items.models import Item
from raid.models import Raid


class Loot(models.Model):
    member = models.ForeignKey('members.Member', on_delete=models.PROTECT)
    raid = models.ForeignKey('raid.Raid', on_delete=models.PROTECT, null=True)
    item = models.ForeignKey('items.Item', on_delete=models.PROTECT)
    price_percentage = models.FloatField(null=True, default=100)
    gp = models.FloatField()
    given_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
