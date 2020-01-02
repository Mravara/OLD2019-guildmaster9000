from django.contrib import admin
from members.models import Member, Character, DecayLog, EPLog
from raid.models import RaidCharacter

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'joined')


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'character_class')


class DecayLogAdmin(admin.ModelAdmin):
    list_display = ('time', 'percentage')


class EPLogAdmin(admin.ModelAdmin):
    list_display = ('raid', 'amount', 'time')


admin.site.register(EPLog, EPLogAdmin)
admin.site.register(DecayLog, DecayLogAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Character, CharacterAdmin)
