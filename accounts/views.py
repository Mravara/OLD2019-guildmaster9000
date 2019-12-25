from django.shortcuts import render, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.conf import settings
from .forms import LoginForm


def welcome(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            return do_login(request, username, password)

    context = {
        'form': LoginForm()
    }
    return render(request, "accounts/index.html", context)


def do_login(request, username, password):
    user = authenticate(request, username=username, password=password)
    if user is not None:
        print('DA')
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        print('ne')
        return HttpResponseRedirect(reverse('welcome'))


def do_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('welcome'))
