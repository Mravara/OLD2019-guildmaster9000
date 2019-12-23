from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from raid.models import Raid
from dungeons.models import Dungeon
from raid.forms import NewRaidForm


def index(request):
    raids = Raid.objects.all().order_by('end')
    context = {
        'raids': raids,
        'breadcrumbs': [
            'Raids'
        ]
    }
    return render(request, "raid/index.html", context)


def get_raid(request, raid_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    return HttpResponse(raid.leader)


def new_raid(request):
    if request.method == 'POST':
        form = NewRaidForm(request.POST)
        
        if form.is_valid():
            context = {
                'breadcrumbs': [
                    'Raid',
                ],
            }
            return render(request, "raid/raid.html", context)

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