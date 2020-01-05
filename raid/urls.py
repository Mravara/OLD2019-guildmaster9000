from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_raid, name='new_raid'),
    path('<int:raid_id>/', views.get_raid, name='raid'),
    path('<int:raid_id>/complete/', views.complete_raid, name='complete'),
    path('<int:raid_id>/pause/', views.pause_raid, name='pause'),
    path('<int:raid_id>/fail/', views.fail_raid, name='fail'),
    path('<int:raid_id>/give_ep/', views.give_ep, name='give_ep'),
    path('<int:raid_id>/give_item/', views.give_item, name='give_item'),
    path('<int:raid_id>/add_raiders/', views.add_raiders, name='add_raiders'),
    path('<int:raid_id>/add_benched_raiders/', views.add_benched_raiders, name='add_benched_raiders'),
    path('<int:raid_id>/delete_loot/<int:loot_id>/', views.delete_loot, name='delete_loot'),
    path('<int:raid_id>/remove_raider/<int:raider_id>/', views.remove_raider, name='remove_raider'),
    path('<int:raid_id>/remove_benched_raider/<int:raider_id>/', views.remove_benched_raider, name='remove_benched_raider'),
    path('<int:raid_id>/ping/', views.ping, name='ping'),
    path('<int:raid_id>/get_items/', views.get_items, name='get_items'),
]