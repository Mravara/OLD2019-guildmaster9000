from django.contrib import admin
from members.models import Member, Character
from raid.models import RaidCharacter

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'joined')


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'character_class')


admin.site.register(Member, MemberAdmin)
admin.site.register(Character, CharacterAdmin)
