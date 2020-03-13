from django.contrib import admin
from .models import Log

class LogAdmin(admin.ModelAdmin):
    list_display = ('raid', 'writer', 'action', 'target_member', 'target', 'value', 'timestamp')

admin.site.register(Log, LogAdmin)

