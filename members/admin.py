from django.contrib import admin
from raid.models import Member, RaidMember

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'joined', 'member_class')

admin.site.register(Member, MemberAdmin)

