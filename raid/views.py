from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


from raid.models import Raid


def index(request):
    raids = Raid.objects.all().order_by('end')
    context = {
        'raids': raids,
        'breadcrumbs': [
            'Raids'
        ]
    }
    return render(request, "raid/index.html", context)


def raid(request, raid_id):
    raid = get_object_or_404(Raid, pk=raid_id)
    return HttpResponse(raid.leader)