from django.contrib import admin
from members.models import Member
from raid.models import RaidMember

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'joined', 'member_class')

admin.site.register(Member, MemberAdmin)

