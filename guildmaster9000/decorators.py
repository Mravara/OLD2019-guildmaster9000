from django.shortcuts import redirect
from members.models import Member

def officers(redirect_url=''):
    def decorator(function):
        def wrap(request, *args, **kwargs):
            member = Member.get_member(request)

            if member.is_officer:
                return function(request, *args, **kwargs)
            else:
                return redirect(redirect_url)

        return wrap
    return decorator
