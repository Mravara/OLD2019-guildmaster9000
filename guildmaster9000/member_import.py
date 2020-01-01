from django.db import models
from django.contrib.auth.models import User
from members.models import Member, Character

import json


file = "/home/mrav/Downloads/Members.json"

with open(file, 'r') as f:
	loaded = json.load(f)
	members = loaded.get('members')
	for m in members:
		member = None
		try:
			member = Member.objects.get(name=m.get('name'))
		except Member.DoesNotExist:
			member = Member.objects.create(name=m.get('name'), ep=m.get('ep'), gp=m.get('gp'))
			print("created new member {}".format(member))
			characters = m.get('characters')
			for character in characters:
				c = Character.objects.create(name=character, owner=member)
				print("created new character {}".format(character))
		try:
			user = User.objects.get(username=m.get('name'))
		except User.DoesNotExist:
			new_user = User.objects.create(username=m.get('name'), password='mljinki8')
			print("created new user {}".format(m.get('name')))
			member.user = new_user
			member.save()

