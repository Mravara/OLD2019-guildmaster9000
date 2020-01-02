from django.contrib import admin
from members.models import Member, Character, Decay, EP
from raid.models import RaidCharacter

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'joined')


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'character_class')


class DecayAdmin(admin.ModelAdmin):
    list_display = ('time', 'percentage')


class EPAdmin(admin.ModelAdmin):
    list_display = ('raid', 'amount', 'time')


admin.site.register(EP, EPAdmin)
admin.site.register(Decay, DecayAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Character, CharacterAdmin)
