from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.timezone import datetime
from django.conf import settings
from django.urls import reverse
from django.db.models import Count, F
from guildmaster9000.decorators import *

from members.models import Member
from raid.models import Raid, RaidMember, BenchedRaidMember
from loot.models import Loot
from items.models import Item, ItemInfo
from dungeons.models import Dungeon
from raid.forms import NewRaidForm, GiveItemForm, GiveEPForm, AddRaidersForm, AddBenchedRaidersForm


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
    form = None
    form_ep = None
    form_add_raiders = None
    form_add_benched_raiders = None
    members = raid.raid_members.all()
    benched_members = raid.benched_raid_members.all()
    if not raid.done:
        items = Item.objects.filter(item_quality__gte=Item.Quality.EPIC)
        form = GiveItemForm()
        form_ep = GiveEPForm()
        form_add_raiders = AddRaidersForm()
        form_add_benched_raiders = AddBenchedRaidersForm()
    context = {
        'raid': raid,
        'loot': loot,
        'items': items,
        'raid_members': members,
        'benched_raid_members': benched_members,
        'form': form,
        'form_ep': form_ep,
        'form_add_raiders': form_add_raiders,
        'form_add_benched_raiders': form_add_benched_raiders,
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
            raid = Raid(dungeon=dung, leader=leader)
            raid.save()

            text_members = form.cleaned_data.get('members')
            text_members_list = text_members.splitlines()
            text_members_list = list(dict.fromkeys(text_members_list)) # removes duplicates

            if len(text_members_list) > 0:
                members = Member.objects.filter(name__in=text_members_list)
                raiders = RaidMember.objects.bulk_create([RaidMember(member=m) for m in members])
                raid.raid_members.set(raiders)
                raid.save()
            else:
                return redirect("/raids/{}/".format(raid.id))
            
            text_benched_members = form.cleaned_data.get('benched_members')
            text_benched_members_list = text_benched_members.splitlines()
            text_benched_members_list = list(dict.fromkeys(text_benched_members_list)) # removes duplicates

            if len(text_benched_members_list) > 0:
                members = Member.objects.filter(name__in=text_benched_members_list)
                raiders = BenchedRaidMember.objects.bulk_create([BenchedRaidMember(member=m) for m in members])
                raid.benched_raid_members.set(raiders)
                raid.raid = raid
                raid.save()

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
            comment = form.cleaned_data.get('comment')
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
                comment=comment,
            )
            loot.save()
        return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def complete_raid(request, raid_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raid.end = datetime.now()
    raid.state = Raid.State.SUCCESS
    raid.raid_members.filter(end=None).update(closed=True, end=datetime.now())
    raid.benched_raid_members.filter(end=None).update(closed=True, end=datetime.now())
    raid.save()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def pause_raid(request, raid_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raid.end = datetime.now()
    raid.state = Raid.State.PAUSED
    raid.raid_members.filter(end=None).update(closed=True, end=datetime.now())
    raid.save()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def fail_raid(request, raid_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raid.end = datetime.now()
    raid.state = Raid.State.FAILED
    raid.raid_members.filter(end=None).update(closed=True, end=datetime.now())
    raid.save()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def remove_raider(request, raid_id, raider_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raider = raid.raid_members.get(id=raider_id)
    raider.end = datetime.now()
    raider.save()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def remove_benched_raider(request, raid_id, raider_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raider = raid.benched_raid_members.get(id=raider_id)
    raider.end = datetime.now()
    raider.save()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def delete_loot(request, raid_id, loot_id):
    loot = get_object_or_404(Loot, pk=loot_id)
    loot.delete()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def give_ep(request, raid_id):
    form = GiveEPForm(request.POST)

    if form.is_valid():
        raid = get_object_or_404(Raid, pk=raid_id)
        raiders = raid.raid_members.all()
        for raider in raiders:
            if not raider.done:
                raider.member.ep = F('ep') + form.cleaned_data.get('ep')
                raider.member.save()

    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def add_raiders(request, raid_id):
    form = AddRaidersForm(request.POST)
    if form.is_valid():
        raid = get_object_or_404(Raid, pk=raid_id)
        text_members = form.cleaned_data.get('members')
        text_members_list = text_members.splitlines()
        text_members_list = list(dict.fromkeys(text_members_list)) # removes duplicates
        members = Member.objects.filter(name__in=text_members_list)
        raiders = RaidMember.objects.bulk_create([RaidMember(member=m) for m in members])
        raid.raid_members.add(*raiders)
        raid.save()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def add_benched_raiders(request, raid_id):
    form = AddBenchedRaidersForm(request.POST)
    if form.is_valid():
        raid = get_object_or_404(Raid, pk=raid_id)
        text_members = form.cleaned_data.get('members')
        text_members_list = text_members.splitlines()
        text_members_list = list(dict.fromkeys(text_members_list)) # removes duplicates
        members = Member.objects.filter(name__in=text_members_list)
        raiders = BenchedRaidMember.objects.bulk_create([BenchedRaidMember(member=m) for m in members])
        raid.benched_raid_members.add(*raiders)
        raid.save()
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def ping(request, raid_id):
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))
    # raid = get_object_or_404(Raid, pk=raid_id)
    # benched_members = raid.benched_members.all()

