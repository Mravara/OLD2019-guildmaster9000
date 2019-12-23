from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from raid.models import Raid
from loot.models import Loot


def loot(request, raid_id=-1):
    if raid_id > -1:
        loot = Loot.objects.filter(raid__pk=raid_id)
    else:
        loot = Loot.objects.all()
    context = {
        'loot': loot,
        'breadcrumbs': [
            'Loot',
        ]
    }
    return render(request, "loot/index.html", context)
