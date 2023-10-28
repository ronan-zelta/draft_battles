from django.urls import path
from . import views

urlpatterns = [
    path('players/', views.PlayerList.as_view(), name='player-list'),
    path('players/<str:uid>/', views.PlayerDetail.as_view(), name='player-detail'),
    path('players/<str:uid>/<int:year>/', views.PlayerYearPoints.as_view(), name='player-year-points'),
]
