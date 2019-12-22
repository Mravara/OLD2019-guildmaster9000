from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:raid_id>/', views.raid, name='raid'),
]