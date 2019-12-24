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
        ARTIFACT = 6

    class ItemType(models.IntegerChoices):
        WEAPONMAINHAND = 0
        TWOHWEAPON = 1
        BODY = 2
        LEGS = 3
        FEET = 4
        ROBE = 5
        CHEST = 6
        NON_EQUIP = 7
        SHIELD = 8
        HAND = 9
        WRIST = 10
        WEAPON = 11
        TRINKET = 12
        TABARD = 13
        BAG = 14
        WAIST = 15
        FINGER = 16
        SHOULDER = 17
        WEAPONOFFHAND = 18
        HOLDABLE = 19
        HEAD = 20
        CLOAK = 21
        NECK = 22
        RANGEDRIGHT = 23
        RANGED = 24
        AMMO = 25
        THROWN = 26
        RELIC = 27


    wow_id = models.IntegerField(default=0)
    name = models.CharField(max_length=128)
    item_quality = models.IntegerField(choices=Quality.choices, null=True)
    item_type = models.IntegerField(choices=ItemType.choices, null=True)
    item_type_name = models.CharField(max_length=256, default='', null=True)
    item_class = models.CharField(max_length=256, default='', null=True)
    item_subclass = models.CharField(max_length=256, default='', null=True)
    item_level = models.IntegerField(null=True)
    ep = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_quality_int(name):
        for integer, choice in Item.Quality.choices:
            if choice.lower() == name.lower():
                return integer
        
        return None

    @staticmethod
    def get_type_int(name):
        for integer, choice in Item.ItemType.choices:
            if choice.lower() == name.lower():
                return integer
        
        return None
