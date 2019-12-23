from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse

from members.models import Member
from raid.models import Raid
from loot.models import Loot
from dungeons.models import Dungeon
from raid.forms import NewRaidForm


def index(request):
    raids = Raid.objects.all().order_by('start')
    context = {
        'raids': raids,
        'breadcrumbs': [
            'Raids'
        ]
    }
    return render(request, "raid/index.html", context)


def get_raid(request, raid_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    loot = Loot.objects.filter(raid=raid)
    context = {
        'raid': raid,
        'loot': loot,
        'breadcrumbs': [
            'Raids',
            raid.dungeon.name,
        ]
    }
    return render(request, "raid/raid.html", context)


def new_raid(request):
    if request.method == 'POST':
        form = NewRaidForm(request.POST)

        if form.is_valid():
            leader = Member.get_current_member(request)
            dung = form.cleaned_data.get('dungeon')
            raid = Raid(dungeon=dung, leader=leader)
            raid.save()
            # return redirect("/raids/{}/".format(raid.id)) radi!
            return HttpResponseRedirect(reverse('raid', args=(raid.id,)))

        return redirect(request.path)

    dungeons = Dungeon.objects.all().order_by('name')
    context = {
        'form': NewRaidForm(),
        'dungeons': dungeons,
        'breadcrumbs': [
            'Raids',
            'New Raid',
        ],
    }
    return render(request, "raid/new_raid.html", context)