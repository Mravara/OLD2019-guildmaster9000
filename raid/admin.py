from django.contrib import admin
from raid.models import Raid


class RaidAdmin(admin.ModelAdmin):
    list_display = ('dungeon', 'start', 'end', 'state')


admin.site.register(Raid, RaidAdmin)