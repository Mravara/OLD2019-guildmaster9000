from django.contrib import admin
from .models import Loot


class LootAdmin(admin.ModelAdmin):
    list_display = ('raid', 'character', 'item', 'comment')


admin.site.register(Loot, LootAdmin)

