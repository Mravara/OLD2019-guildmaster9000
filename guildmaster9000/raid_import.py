from django.db import models
from raid.models import Raid, RaidCharacter
from loot.models import Loot
from members.models import Member, Character
from dungeons.models import Dungeon
from items.models import Item, ItemInfo
import datetime
import re

import json


file = "/home/mrav/Downloads/Output.json"

with open(file, 'r') as f:
    loaded = json.load(f)
    raids = loaded.get('raids')
    dungeon = Dungeon.objects.all().first()
    for r in raids:
        raiders = []
        date = datetime.datetime.strptime(r.get('date'), '%d.%m.%Y.')
        characters_text = r.get('characters')
        characters = Character.objects.filter(name__in=characters_text)
        for c in characters:
            raider = RaidCharacter.objects.create(character=c, start=date, end=date, closed=True)
            raiders.append(raider)
        leader = Member.objects.get(pk=11)
        raid = Raid.objects.create(dungeon=dungeon, leader=leader, state=3, start=date, end=date)
        raid.raid_characters.set(raiders)

        raid_loot = r.get('loot')
        for l in raid_loot:
            try:        
                item = Item.objects.get(name=l.get('item'))
                item_info = ItemInfo.objects.get(pk=1)
                given_to = Character.objects.get(name=l.get('given_to'))
                loot = Loot.objects.create(character=given_to, raid=raid, item=item, item_info=item_info, price_percentage=100, given_by=leader, timestamp=date)
            except:
                print("doesn't exist: " + l.get('given_to'))
        








    # text = f.read()
    # replaced = []
    # # add " " to items
    # reg = r'\"item\"\:\ ([^,^"]+)'
    # results = re.findall(reg, text)
    # for r in results:
    #     if r not in replaced:
    #         text = text.replace(r, '"{}"'.format(r))
    #         replaced.append(r)
    
    # with open("/home/mrav/Downloads/Output.json", "w") as outp:
    #     outp.write(text)