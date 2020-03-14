from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='officers_index'),
    path('decay_epgp/', views.decay_epgp, name='decay_epgp'),
    path('new_member/', views.new_member, name='new_member'),
    path('logs/', views.logs, name='logs'),
    path('logs/page/', views.get_page, name='page'),
]
