from django.urls import path
from . import views


urlpatterns = [
    path('', views.loot, name='loot'),
    path('<int:raid_id>/', views.loot, name='loot'),
]