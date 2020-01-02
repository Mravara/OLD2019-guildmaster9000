from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.utils.timezone import datetime
from members.models import Member, DecayLog
from guildmaster9000.decorators import *
from officers.forms import DecayForm


@officers('/')
def index(request):
    form = DecayForm()
    context = {
        'form': form,
    }
    return render(request, "officers/index.html", context)


@officers('/')
def decay_epgp(request):
    form = DecayForm(request.POST)
    if form.is_valid():
        decay = form.cleaned_data.get('decay')
        members = Member.objects.all()
        members.update(ep=F('ep') * (1 - decay/100), gp=F('gp') * (1 - decay/100))
        decay = DecayLog.objects.create(percentage=decay, time=datetime.now())
        decay.affected_members.set(members)
        decay.save()
    return HttpResponseRedirect(reverse('officers_index'))