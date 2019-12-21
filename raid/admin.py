from django.contrib import admin
from raid.models import Member, RaidMember, Raid, Dungeon, Item, Loot, BenchedRaidMember

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'joined')

admin.site.register(Member, MemberAdmin)
admin.site.register(Raid)
admin.site.register(RaidMember)
admin.site.register(Dungeon)
admin.site.register(Item)
admin.site.register(Loot)
admin.site.register(BenchedRaidMember)


