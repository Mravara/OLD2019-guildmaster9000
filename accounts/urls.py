from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.welcome, name='welcome'),
    path('logout/', views.do_logout, name='logout'),
]