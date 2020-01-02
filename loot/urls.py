from django.urls import path
from . import views


urlpatterns = [
    path('', views.loot, name='loot'),
    path('page/', views.get_page, name='page'),
]