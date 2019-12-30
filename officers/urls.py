from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('decay_epgp/', views.decay_epgp, name='decay_epgp'),
]