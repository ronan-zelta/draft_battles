from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('play/', views.play_game, name='play_game'),
]