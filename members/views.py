from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.utils.timezone import datetime
from members.models import Member
from django.db.models import Max, Min, F


def index(request):
    members = Member.objects.all().order_by('name')
    members = members.annotate(sum=F('ep') / F('gp'))
    min_prio = members.aggregate(Min('sum')).get('sum__min')
    max_prio = members.aggregate(Max('sum')).get('sum__max')
    print(min_prio)
    print(max_prio)
    context = {
        'members': members,
        'timestamp': datetime.now(),
        'min_priority': min_prio,
        'max_priority': max_prio,
        'breadcrumbs': [
            'Members'
        ]
    }
    return render(request, "members/index.html", context)


def member(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    return HttpResponse(member.name)

