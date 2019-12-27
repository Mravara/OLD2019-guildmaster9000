from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.timezone import datetime
from django.conf import settings
from django.urls import reverse
from django.db.models import Count
from guildmaster9000.decorators import *

from members.models import Member
from raid.models import Raid, RaidMember
from loot.models import Loot
from items.models import Item, ItemInfo
from dungeons.models import Dungeon
from raid.forms import NewRaidForm, GiveItemForm


def index(request):
    raids = Raid.objects.order_by('-start').annotate(total_items=Count('loot'))
    context = {
        'raids': raids,
        'breadcrumbs': [
            'Raids'
        ]
    }
    return render(request, "raid/index.html", context)


def get_raid(request, raid_id):
    referer = request.META.get('HTTP_REFERER')
    raid = get_object_or_404(Raid, pk=raid_id)
    loot = Loot.objects.filter(raid=raid)
    items = None
    members = None
    form = None
    members = raid.raid_members.filter(end=None)
    if raid.end is None:
        items = Item.objects.filter(item_quality__gte=Item.Quality.EPIC)
        form = GiveItemForm()
    context = {
        'raid': raid,
        'loot': loot,
        'items': items,
        'raid_members': members,
        'form': form,
        'item_types': ItemInfo.ItemSlot.choices,
        'breadcrumbs': [
            'Raids' if 'raids' in referer else 'Loot',
            raid.dungeon.name,
        ]
    }
    return render(request, "raid/raid.html", context)


@officers('/raids/')
def new_raid(request):
    if request.method == 'POST':
        form = NewRaidForm(request.POST)

        if form.is_valid():
            leader = request.user.member
            dung = form.cleaned_data.get('dungeon')
            text_members = form.cleaned_data.get('members')
            text_members_list = text_members.splitlines()
            raid = Raid(dungeon=dung, leader=leader)
            raid.save()
            if len(text_members_list) > 0:
                members = Member.objects.filter(name__in=text_members_list)
                raiders = RaidMember.objects.bulk_create([RaidMember(member=m) for m in members])
                raid.raid_members.set(raiders)
                raid.save()
            # return redirect("/raids/{}/".format(raid.id)) radi!
            return HttpResponseRedirect(reverse('raid', args=(raid.id,)))

        return redirect(request.path)

    context = {
        'form': NewRaidForm(),
        'breadcrumbs': [
            'Raids',
            'New Raid',
        ],
    }
    return render(request, "raid/new_raid.html", context)


@officers('/raids/')
def give_item(request, raid_id):
    if request.method == 'POST':
        form = GiveItemForm(request.POST)
        if form.is_valid():
            member_id = form.cleaned_data.get('member_id')
            item_id = form.cleaned_data.get('item_id')
            item_info = form.cleaned_data.get('item_slot')
            raid = get_object_or_404(Raid, pk=raid_id)
            member = get_object_or_404(Member, pk=member_id)
            item = get_object_or_404(Item, pk=item_id)
            price_percentage = form.cleaned_data.get('price')
            member.save()
            loot = Loot(
                member=member,
                raid=raid,
                item=item,
                item_info=item_info,
                price_percentage=price_percentage,
                given_by=request.user,
            )
            loot.save()
        return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


def complete_raid(request, raid_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raid.end = datetime.now()
    raid.state = Raid.State.SUCCESS
    raid.raid_members.filter(end=None).update(closed=True, end=datetime.now())
    raid.save()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


def pause_raid(request, raid_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raid.end = datetime.now()
    raid.state = Raid.State.PAUSED
    raid.raid_members.filter(end=None).update(closed=True, end=datetime.now())
    raid.save()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


def fail_raid(request, raid_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raid.end = datetime.now()
    raid.state = Raid.State.FAILED
    raid.raid_members.filter(end=None).update(closed=True, end=datetime.now())
    raid.save()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


def remove_raider(request, raid_id, raider_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raider = raid.raid_members.get(id=raider_id)
    raider.end = datetime.now()
    raider.save()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


def delete_loot(request, raid_id, loot_id):
    loot = get_object_or_404(Loot, pk=loot_id)
    loot.delete()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))