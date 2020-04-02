from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404, JsonResponse
from django.utils.timezone import datetime
from django.conf import settings
from django.urls import reverse
from django.db.models import Count, F, Sum
from django.core import serializers
from django.contrib import messages
import requests

from guildmaster9000.decorators import *
from itertools import chain

from members.models import Member, Character
from raid.models import Raid, RaidCharacter, BenchedRaidCharacter
from loot.models import Loot
from items.models import Item, ItemInfo
from dungeons.models import Dungeon
from officers.models import Log
from raid.forms import NewRaidForm, GiveItemForm, GiveEPForm, AddRaidersForm, AddBenchedRaidersForm


def index(request):
    raids = Raid.objects.order_by('-start').annotate(total_items=Count('loot')).select_related('dungeon', 'leader').prefetch_related('raidcharacter')
    context = {
        'raids': raids,
        'breadcrumbs': [
            'Raids'
        ]
    }
    return render(request, "raid/index.html", context)


def get_raid(request, raid_id):
    referer = request.META.get('HTTP_REFERER')
    raid = None
    try:
        raid = Raid.objects.select_related('leader', 'dungeon').get(pk=raid_id)
    except Raid.DoesNotExist:
        raise Http404("WTF?")
    loot = Loot.objects.filter(raid=raid).select_related('item', 'character', 'item_info', 'given_by')
    form = None
    form_ep = None
    form_add_raiders = None
    form_add_benched_raiders = None
    
    characters = RaidCharacter.objects.filter(raid=raid).select_related('character__owner')
    
    benched_characters = BenchedRaidCharacter.objects.filter(raid=raid).select_related('character__owner')
    
    all_characters_query = Character.objects.all().order_by('name')
    raid_characters_query = characters.order_by('character__name')

    min_priority = 9999999
    max_priority = -1

    for character in characters:
        if character.character.owner.priority < min_priority:
            min_priority = character.character.owner.priority
        if character.character.owner.priority > max_priority:
            max_priority = character.character.owner.priority


    if not raid.done or raid.editing:
        form = GiveItemForm()
        form.fields['character'].queryset = raid_characters_query
        form_ep = GiveEPForm()
        form_ep.fields['character'].queryset = raid_characters_query
        form_add_raiders = AddRaidersForm()
        form_add_raiders.fields['character'].queryset = all_characters_query
        form_add_benched_raiders = AddBenchedRaidersForm()
        form_add_benched_raiders.fields['character'].queryset = all_characters_query
    context = {
        'raid': raid,
        'loot': loot,
        'raid_characters': characters,
        'benched_raid_characters': benched_characters,
        'min_priority': min_priority,
        'max_priority': max_priority,
        'form': form,
        'form_ep': form_ep,
        'form_add_raiders': form_add_raiders,
        'form_add_benched_raiders': form_add_benched_raiders,
        'item_types': ItemInfo.ItemSlot.choices,
        'breadcrumbs': [
            'Raids' if (referer is not None and 'raids' in referer) else 'Loot',
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

            Log.objects.create(
                writer=request.user.member,
                action=Log.Action.CREATE_RAID,
                raid=raid
            )

            text_members = form.cleaned_data.get('members')
            text_members_list = text_members.splitlines()
            text_members_list.append('GuildBank')
            text_members_list = list(dict.fromkeys(text_members_list)) # removes duplicates
            text_members_list = [x.capitalize().strip() for x in text_members_list]

            raiders = None
            benched_raiders = None

            if len(text_members_list) > 0:
                raiders = characters = Character.objects.filter(name__in=text_members_list)
                RaidCharacter.objects.bulk_create([RaidCharacter(character=c, raid=raid) for c in characters])
            else:
                return redirect("/raids/{}/".format(raid.id))
            
            text_benched_members = form.cleaned_data.get('benched_members')
            text_benched_members_list = text_benched_members.splitlines()
            text_benched_members_list = list(dict.fromkeys(text_benched_members_list)) # removes duplicates

            if len(text_benched_members_list) > 0:
                benched_raiders = characters = Character.objects.filter(name__in=text_benched_members_list)
                BenchedRaidCharacter.objects.bulk_create([BenchedRaidCharacter(character=c, raid=raid) for c in characters])

            # # trigger webhook
            # webhook_url = 'https://discordapp.com/api/webhooks/663807443783909412/oaQIP-kuEz4VWGvtpsITdgb2mjpI2HtIktuHQ8ADlRS7dWWFkxEH76RGMPDthg8uZlhn'
            # data = 'New raid started\n'
            # ids = []
            
            # if raiders:
            #     for raider in raiders:
            #         ids.append(str(raider.owner.discord_id))
            
            # if benched_raiders:
            #     for benched_raider in benched_raiders:
            #         ids.append(str(benched_raider.owner.discord_id))
            
            # id_list = '\n'.join(ids)
            # data = data + id_list
            # webhook_data = {
            #     'content': data
            # }
            # requests.post(webhook_url, webhook_data)
            messages.success(request, "Raid created.")
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
def start_raid(request, raid_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raid.state = Raid.State.IN_PROGRESS
    raid.start = datetime.now()
    raid.save()
    
    RaidCharacter.objects.filter(raid=raid, end=None).update(start=raid.start)
    BenchedRaidCharacter.objects.filter(raid=raid, end=None).update(start=raid.start)
   
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def give_item(request, raid_id):
    if request.method == 'POST':
        form = GiveItemForm(request.POST)
        if form.is_valid():
            character = form.cleaned_data.get('character')
            item_id = form.cleaned_data.get('item_id')
            item_info = form.cleaned_data.get('item_slot')
            comment = form.cleaned_data.get('comment')
            raid = get_object_or_404(Raid, pk=raid_id)
            item = get_object_or_404(Item, pk=item_id)
            price_percentage = form.cleaned_data.get('price')
            loot = Loot(
                character=character.character,
                raid=raid,
                item=item,
                item_info=item_info,
                price_percentage=price_percentage,
                given_by=request.user.member,
                comment=comment,
            )
            loot.save()
            character.character.owner.set_gp(F('gp') + loot.gp)
            character.character.owner.save()

            Log.objects.create(
                writer=request.user.member,
                target=character.character,
                target_member=character.character.owner,
                action=Log.Action.GIVE_LOOT,
                raid=raid,
                item=item,
                value='Price Percentage: {0}, GP: {1}, Comment: {2}'.format(price_percentage, loot.gp, comment)
            )

            messages.success(request, "Item <strong>{0}</strong> given to <strong>{1}</strong> for <strong>{2}%</strong> of the price.".format(item.name, character.character.name, price_percentage))
        return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def complete_raid(request, raid_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    was_editing = raid.state == Raid.State.EDITING
    raid.state = Raid.State.SUCCESS
    if not was_editing:
        raid.end = datetime.now()
        raid_duration = (raid.end - raid.start).total_seconds() / 60.0
        
        raiders = RaidCharacter.objects.filter(raid=raid)
        benched_raiders = BenchedRaidCharacter.objects.filter(raid=raid)

        for raider in raiders:
            if raider.end is None:
                raider.end = raid.end
                raider.closed = True
            duration = (raider.end - raider.start).total_seconds() / 60.0
            end_ep = (duration/raid_duration) * raid.dungeon.ep_worth
            ep = raider.earned_ep + end_ep
            raider.earned_ep = ep
            raider.save()
            raider.character.owner.ep = raider.character.owner.ep + end_ep
            raider.character.owner.save()

        for benched_raider in benched_raiders:
            if benched_raider.end is None:
                benched_raider.end = raid.end
                benched_raider.closed = True
            duration = (benched_raider.end - benched_raider.start).total_seconds() / 60.0
            end_ep = (duration/raid_duration) * raid.dungeon.ep_worth
            ep = benched_raider.earned_ep + end_ep
            benched_raider.earned_ep = ep
            benched_raider.save()
            benched_raider.character.owner.ep = benched_raider.character.owner.ep + end_ep
            benched_raider.character.owner.save()

        # RaidCharacter.objects.filter(raid=raid, end=None).update(closed=True, earned_ep=F('earned_ep') + ep, end=datetime.now())
        # BenchedRaidCharacter.objects.filter(raid=raid, end=None).update(closed=True, earned_ep=F('earned_ep') + ep, end=datetime.now())
    raid.save()

    Log.objects.create(
        writer=request.user.member,
        action=Log.Action.END_RAID,
        raid=raid,
        value='complete'
    )

    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


# @officers('/raids/')
# def pause_raid(request, raid_id):
#     raid = get_object_or_404(Raid, pk=raid_id)
#     was_editing = raid.state == Raid.State.EDITING
#     raid.state = Raid.State.PAUSED
#     if not was_editing:
#         raid.end = datetime.now()
#         RaidCharacter.objects.filter(raid=raid, end=None).update(closed=True, end=datetime.now())
#         BenchedRaidCharacter.objects.filter(raid=raid, end=None).update(closed=True, end=datetime.now())
#     raid.save()

#     Log.objects.create(
#         writer=request.user.member,
#         action=Log.Action.END_RAID,
#         raid=raid,
#         value='pause'
#     )

#     return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


# @officers('/raids/')
# def fail_raid(request, raid_id):
#     raid = get_object_or_404(Raid, pk=raid_id)
#     was_editing = raid.state == Raid.State.EDITING
#     raid.state = Raid.State.FAILED
#     if not was_editing:
#         raid.end = datetime.now()
#         RaidCharacter.objects.filter(raid=raid, end=None).update(closed=True, end=datetime.now())
#         BenchedRaidCharacter.objects.filter(raid=raid, end=None).update(closed=True, end=datetime.now())
#     raid.save()

#     Log.objects.create(
#         writer=request.user.member,
#         action=Log.Action.END_RAID,
#         raid=raid,
#         value='fail'
#     )

#     return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def bench_raider(request, raid_id, raider_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raider = RaidCharacter.objects.get(id=raider_id, raid=raid)
    end = datetime.now()
    raider.end = end
    raider.save()
    obj, created = BenchedRaidCharacter.objects.get_or_create(character=raider.character, raid=raid, end__isnull=True)
    if not created:
        messages.error(request, "<strong>{0}</strong> is already on the bench.".format(raider.character.name))
    else:
        messages.success(request, "<strong>{0}</strong> is warming the bench.".format(raider.character.name))

        Log.objects.create(
            writer=request.user.member, 
            target=raider.character, 
            target_member=raider.character.owner, 
            action=Log.Action.BENCH,
            raid=raid
        )

    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def unbench_raider(request, raid_id, raider_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raider = BenchedRaidCharacter.objects.get(id=raider_id, raid=raid)
    end = datetime.now()
    raider.end = end
    raider.save()
    obj, created = RaidCharacter.objects.get_or_create(character=raider.character, raid=raid, end__isnull=True)
    if not created:
        messages.error(request, "<strong>{0}</strong> is already in the raid.".format(raider.character.name))
    else:
        messages.success(request, "<strong>{0}</strong> is now in the raid.".format(raider.character.name))

        Log.objects.create(
            writer=request.user.member, 
            target=raider.character, 
            target_member=raider.character.owner, 
            action=Log.Action.UNBENCH,
            raid=raid
        )

    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def remove_raider(request, raid_id, raider_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raider = RaidCharacter.objects.get(id=raider_id, raid=raid)
    raider.end = datetime.now()
    raider.save()

    Log.objects.create(
        writer=request.user.member, 
        target=raider.character, 
        target_member=raider.character.owner, 
        action=Log.Action.REMOVE_FROM_RAID,
        raid=raid
    )

    messages.success(request, "<strong>{0}</strong> has been removed from the raid.".format(raider.character.name))
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def remove_benched_raider(request, raid_id, raider_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raider = BenchedRaidCharacter.objects.get(id=raider_id, raid=raid)
    raider.end = datetime.now()
    raider.save()

    Log.objects.create(
        writer=request.user.member, 
        target=raider.character, 
        target_member=raider.character.owner, 
        action=Log.Action.REMOVE_FROM_RAID,
        raid=raid,
        value="bench"
    )

    messages.success(request, "<strong>{0}</strong> has been removed from the raid bench.".format(raider.character.name))
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def delete_loot(request, raid_id, loot_id):
    loot = get_object_or_404(Loot, pk=loot_id)
    loot.character.owner.set_gp(F('gp') - loot.gp)
    loot.character.owner.save()
    loot.delete()
    item_name = loot.item.name

    Log.objects.create(
        writer=request.user.member, 
        target=loot.character, 
        target_member=loot.character.owner, 
        action=Log.Action.DELETE_LOOT,
        raid=loot.raid,
        value=str(-loot.gp)
    )

    messages.success(request, "<strong>{0}</strong> has been deleted from the loot table.".format(item_name))
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def give_ep(request, raid_id):
    form = GiveEPForm(request.POST)
    if form.is_valid():
        ep = form.cleaned_data.get('ep')
        character = form.cleaned_data.get('character')
        raid = get_object_or_404(Raid, pk=raid_id)
        only_present = form.cleaned_data.get('only_present')

        if character is not None:
            character.character.owner.ep = F('ep') + ep
            character.character.owner.save()
            character.earned_ep = F('earned_ep') + ep
            character.save()
            Log.objects.create(
                writer=request.user.member, 
                target=character.character, 
                target_member=character.character.owner, 
                action=Log.Action.GIVE_EP,
                raid=raid,
                value=ep
            )
        else:
            raiders = RaidCharacter.objects.filter(raid=raid).select_related('character__owner')
            if only_present:
                raiders = raiders.filter(end=None)
            raiders.update(earned_ep=F('earned_ep') + ep)
            for raider in raiders:
                raider.character.owner.ep = F('ep') + ep
                raider.character.owner.save()
                Log.objects.create(
                    writer=request.user.member, 
                    target=raider.character, 
                    target_member=raider.character.owner, 
                    action=Log.Action.GIVE_EP,
                    raid=raid,
                    value=ep
                )
            
            benched_raiders = BenchedRaidCharacter.objects.filter(raid=raid).select_related('character__owner')
            if only_present:
                benched_raiders = benched_raiders.filter(end=None)
            benched_raiders.update(earned_ep=F('earned_ep') + ep)
            for benched_raider in benched_raiders:
                benched_raider.character.owner.ep = F('ep') + ep
                benched_raider.character.owner.save()
                Log.objects.create(
                    writer=request.user.member, 
                    target=benched_raider.character, 
                    target_member=benched_raider.character.owner, 
                    action=Log.Action.GIVE_EP,
                    raid=raid,
                    value=ep
                )

        if character is None:
            if only_present:
                messages.success(request, "<strong>{0} EP</strong> has been given to every <strong>currently present</strong> raid member.".format(ep))
            else:
                messages.success(request, "<strong>{0} EP</strong> has been given to <strong>every</strong> raid member.".format(ep))
        else:
            messages.success(request, "<strong>{0} EP</strong> has been given to <strong>{1}</strong>.".format(ep, character.character.name))
    else:
        messages.error(request, "Something went wrong :(")
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def add_raiders(request, raid_id):
    form = AddRaidersForm(request.POST)
    if form.is_valid():
        raid = get_object_or_404(Raid, pk=raid_id)
        character = form.cleaned_data.get('character')

        if character is not None:
            obj, created = RaidCharacter.objects.get_or_create(character=character, raid=raid, end__isnull=True)
            
            if not created:
                messages.error(request, "<strong>{0}</strong> is already in this raid.".format(character.name))
                return HttpResponseRedirect(reverse('raid', args=(raid_id,)))

            Log.objects.create(
                    writer=request.user.member, 
                    target=character, 
                    target_member=character.owner, 
                    action=Log.Action.ADD_TO_RAID,
                    raid=raid
                )

            messages.success(request, "<strong>{0}</strong> has been added to the raid.".format(character.name))
        else:
            text_members = form.cleaned_data.get('members')
            text_members_list = text_members.splitlines()
            text_members_list = list(dict.fromkeys(text_members_list)) # removes duplicates
            text_members_list = [x.capitalize().strip() for x in text_members_list]

            characters = Character.objects.filter(name__in=text_members_list)

            count = 0
            for c in characters:
                obj, created = RaidCharacter.objects.get_or_create(character=c, raid=raid, end__isnull=True)
                if not created:
                    messages.error(request, "<strong>{0}</strong> is already in this raid.".format(c.name))
                else:
                    count += 1

                    Log.objects.create(
                        writer=request.user.member, 
                        target=c, 
                        target_member=c.owner, 
                        action=Log.Action.ADD_TO_RAID,
                        raid=raid
                    )

            if count > 0:
                messages.success(request, "<strong>{0}</strong> new raiders have been added to the raid.".format(count))
    else:
        messages.error(request, "Something went wrong :(")
        
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def add_benched_raiders(request, raid_id):
    form = AddBenchedRaidersForm(request.POST)
    if form.is_valid():
        raid = get_object_or_404(Raid, pk=raid_id)
        character = form.cleaned_data.get('character')

        if character is not None:
            obj, created = BenchedRaidCharacter.objects.get_or_create(character=character, raid=raid, end__isnull=True)
            if not created:
                messages.error(request, "<strong>{0}</strong> is already in this raid.".format(character.name))
                return HttpResponseRedirect(reverse('raid', args=(raid_id,)))

            Log.objects.create(
                writer=request.user.member, 
                target=character, 
                target_member=character.owner, 
                action=Log.Action.ADD_TO_RAID,
                raid=raid,
                value='bench'
            )

            messages.success(request, "<strong>{0}</strong> has been added to the raid.".format(character.name))
        else:
            text_members = form.cleaned_data.get('members')
            text_members_list = text_members.splitlines()
            text_members_list = list(dict.fromkeys(text_members_list)) # removes duplicates
            characters = Character.objects.filter(name__in=text_members_list)
            count = 0
            for c in characters:
                obj, created = BenchedRaidCharacter.objects.get_or_create(character=c, raid=raid, end__isnull=True)
                if not created:
                    messages.error(request, "<strong>{0}</strong> is already in this raid.".format(c.name))
                else:
                    count += 1

                    Log.objects.create(
                        writer=request.user.member, 
                        target=c, 
                        target_member=c.owner, 
                        action=Log.Action.ADD_TO_RAID,
                        raid=raid,
                        value='bench'
                    )

            if count > 0:
                messages.success(request, "<strong>{0}</strong> new raiders have been added to the raid (benched).".format(count))
    else:
        messages.error(request, "Something went wrong :(")
    
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))


@officers('/raids/')
def ping(request, raid_id):
    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))
    # raid = get_object_or_404(Raid, pk=raid_id)
    # benched_members = raid.benched_members.all()


@officers('/raids/')
def get_items(request, raid_id):
    term = request.GET.get('term')
    items = Item.objects.filter(name__icontains=term, item_quality__gte=Item.Quality.EPIC).values('id', value=F('name')).order_by('name')
    data = []
    for i in items:
        data.append(i)
    return JsonResponse(data, safe=False)


@officers('/raids/')
def unlock_raid(request, raid_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    raid.state = Raid.State.EDITING
    raid.save()

    Log.objects.create(
        writer=request.user.member, 
        action=Log.Action.UNLOCK_RAID,
        raid=raid
    )

    return HttpResponseRedirect(reverse('raid', args=(raid_id,)))

