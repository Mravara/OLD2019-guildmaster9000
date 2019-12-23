from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):

    class Rank(models.IntegerChoices):
        MEMBER = 0,
        RAID_LEADER = 10
        OFFICER = 100
        ADMIN = 1000

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    discord_id = models.BigIntegerField(null=True)
    name = models.CharField(max_length=50)
    rank = models.IntegerField(choices=Rank.choices, default=Rank.MEMBER)
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_current_member(request):
        return Member.objects.get(user=request.user)
