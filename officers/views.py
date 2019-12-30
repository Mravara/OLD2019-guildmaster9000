from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.utils.timezone import datetime

from members.models import Member, Decay
from guildmaster9000.decorators import *


def index(request):
    return HttpResponse('officers')


@officers('/')
def decay_epgp(request, percentage=10):
    print("decay happened")
    members = Member.objects.all()
    members.update(ep=F('ep') * (1 - percentage/100), gp=F('gp') * (1 - percentage/100))
    decay = Decay.objects.create(percentage=percentage, time=datetime.now())
    decay.affected_members.set(members)
    decay.save()
    return HttpResponseRedirect(reverse('index'))