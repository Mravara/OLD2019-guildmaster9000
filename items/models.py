from django.shortcuts import get_object_or_404
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
    gp = models.IntegerField(default=0, null=True)

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


    def get_item_value(self):
        if self.item_quality == Item.Quality.UNCOMMON:
            return (self.item_level - 4) / 2
        elif self.item_quality == Item.Quality.RARE:
            return (self.item_level - 1.82) / 1.6
        elif self.item_quality == Item.Quality.EPIC:
            return (self.item_level - 1.3) / 1.3
        elif self.item_quality == Item.Quality.LEGENDARY:
            return (self.item_level - 1.265642857) / 1.0725



class ItemInfo(models.Model):

    def __str__(self):
        return self.name
    
    class ItemSlot(models.IntegerChoices):
        TwoHandMelee = 0
        RangedHunter = 1
        TwoHandCaster = 2
        OneHandMelee = 3
        OneHandCaster = 4
        ShieldMelee = 5
        Head = 6
        Chest = 7
        Legs = 8
        Shoulder = 9
        Hands = 10
        Waist = 11
        Feet = 12
        TwoHandHunter = 13
        Wand = 14
        ShieldCaster = 15
        Trinket = 16
        Wrist = 17
        Neck = 18
        Back = 19
        Finger = 20
        RangedMelee = 21
        OneHandHunter = 22
        OffHandCaster = 23
        Relic = 24

    name = models.CharField(max_length=128)
    slot_value = models.FloatField()
    slot_ref = models.IntegerField(choices=ItemSlot.choices)