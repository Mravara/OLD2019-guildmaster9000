from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.utils.timezone import datetime
from members.models import Member


def index(request):
    members = Member.objects.all().order_by('name')
    context = {
        'members': members,
        'timestamp': datetime.now(),
        'breadcrumbs': [
            'Members'
        ]
    }
    return render(request, "members/index.html", context)


def member(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    return HttpResponse(member.name)

