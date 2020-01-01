from django.contrib import admin
from members.models import Member, Character, Decay
from raid.models import RaidCharacter

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'joined')


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'character_class')


class DecayAdmin(admin.ModelAdmin):
    list_display = ('time', 'percentage', 'affected_members')


admin.site.register(Decay)
admin.site.register(Member, MemberAdmin)
admin.site.register(Character, CharacterAdmin)
