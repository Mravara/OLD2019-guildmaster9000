from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='officers_index'),
    path('decay_epgp/', views.decay_epgp, name='decay_epgp'),
]