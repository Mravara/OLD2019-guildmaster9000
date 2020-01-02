from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from raid.models import Raid
from loot.models import Loot


def loot(request):
    all_loot = Loot.objects.all()
    context = {
        'loot': all_loot,
        'breadcrumbs': [
            'Loot',
        ]
    }
    return render(request, "loot/index.html", context)


def get_page(request):
    columns = []
    draw = request.GET.get('draw')
    start = int(request.GET.get('start')[0])
    end = start + int(request.GET.get('length')[0]) * 10 # wtf?
    search = request.GET.get('search[value]')

    loot = Loot.objects.all().filter(Q(character__name__icontains=search) | Q(item__name__icontains=search))[start:end]

    for l in loot:
        row = [
            l.raid.dungeon.name, 
            l.character.owner.name, 
            l.character.name, 
            l.character.character_class, 
            "<a href='https://classic.wowhead.com/item={}' class='q1'>{}</a>".format(l.item.wow_id, l.item.name),
            round(l.gp, 2),
            l.timestamp.strftime("%Y-%m-%d %H:%Mh")
        ]
        columns.append(row)

    count = Loot.objects.all().count()

    data = {
        'draw': draw,
        'recordsTotal': count,
        'recordsFiltered': count,
        'data': columns,
    }
    return JsonResponse(data)