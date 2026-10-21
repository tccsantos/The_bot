from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('pre_game/', views.pre_game, name="pre_game"),
    path('game/', views.game, name="game"),
    path('pos_game/', views.pos_game, name="pos_game"),
    path('history/', views.game_history, name="game_history"),
]