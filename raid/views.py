# from django.shortcuts import render
from django.http import HttpResponse


def members(request):
    return HttpResponse("Here are members")

