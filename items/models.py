from django.conf import settings
from django.db import models


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
    quality = models.IntegerField(choices=Quality.choices, null=True)
    ep = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.name