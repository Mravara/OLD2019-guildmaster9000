from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.timezone import datetime
from django.conf import settings
from django.urls import reverse

from members.models import Member
from raid.models import Raid
from loot.models import Loot
from items.models import Item
from dungeons.models import Dungeon
from raid.forms import NewRaidForm, GiveItemForm


def index(request):
    raids = Raid.objects.order_by('-start')
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
    items = None
    members = None
    form = None
    if raid.end is None:
        items = Item.objects.filter(item_quality__gte=Item.Quality.EPIC)
        members = Member.objects.all()
        form = GiveItemForm()
        form.initial['raid'] = raid_id
    context = {
        'raid': raid,
        'loot': loot,
        'items': items,
        'members': members,
        'form': form,
        'item_types': Item.ItemType.choices,
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


def give_item(request, raid_id):
    if request.method == 'POST':
        form = GiveItemForm(request.POST)
        if form.is_valid():
            member_id = form.cleaned_data.get('member_id')
            item_id = form.cleaned_data.get('item_id')
            raid = get_object_or_404(Raid, pk=raid_id)
            member = get_object_or_404(Member, pk=member_id)
            item = get_object_or_404(Item, pk=item_id)
            price_percentage = form.cleaned_data.get('price')

            loot = Loot(
                member=member,
                raid=raid,
                item=item,
                price_percentage=price_percentage,
                gp=10,
                given_by=request.user,
            )
            loot.save()
        return HttpResponseRedirect(reverse('raid', args=(raid.id,)))


def complete_raid(request, raid_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raid.end = datetime.now()
    raid.state = Raid.State.SUCCESS
    raid.save()
    return HttpResponseRedirect(reverse('raid', args=(raid.id,)))


def pause_raid(request, raid_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raid.end = datetime.now()
    raid.state = Raid.State.PAUSED
    raid.save()
    return HttpResponseRedirect(reverse('raid', args=(raid.id,)))

def fail_raid(request, raid_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raid.end = datetime.now()
    raid.state = Raid.State.FAILED
    raid.save()
    return HttpResponseRedirect(reverse('raid', args=(raid.id,)))