from django.db import models
from django.contrib.auth.models import User
from members.models import Member, Character

import json


file = "/home/mrav/Downloads/Primal_ExtractChars.json"

Character.objects.all().delete()
Member.objects.all().delete()

def get_class_int(class_string):
        if class_string == "Druid":
            return 0
        elif class_string == "Hunter":
            return 1
        elif class_string == "Mage":
            return 2
        elif class_string == "Priest":
            return 3
        elif class_string == "Rogue":
            return 4
        elif class_string == "Shaman":
            return 5
        elif class_string == "Warlock":
            return 6
        elif class_string == "Warrior":
            return 7
        else:
            return 0

with open(file, 'r') as f:
	loaded = json.load(f)
	members = loaded.get('members')
	for m in members:
		member = None
		try:
			member = Member.objects.get(name=m.get('name'))
			member.ep = m.get('ep')
			member.gp = m.get('gp')
		except Member.DoesNotExist:
			member = Member.objects.create(name=m.get('name'), ep=m.get('ep'), gp=m.get('gp'))
			print("created new member {}".format(member))

		characters = m.get('characters')
		for character in characters:
			if character.get('name') != '':
				c = Character.objects.create(name=character.get('name'), character_class=get_class_int(character.get('class')), owner=member)
				print("created new character {}".format(character))
		try:
			user = User.objects.get(username=m.get('name'))
			member.user = user
		except User.DoesNotExist:
			new_user = User.objects.create(username=m.get('name'), password='mljinki8')
			print("created new user {}".format(m.get('name')))
			member.user = new_user
		member.save()

