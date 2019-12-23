from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
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
