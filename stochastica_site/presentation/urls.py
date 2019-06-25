from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('play/<game_id>/', views.slide, name='slide'),
    path('next_round/<game_id>', views.next_round, name='next_round'),
    path('play/<game_id>/next_round', views.next_round, name='next_round_2'), # Need to fix this, just a dumb js thing
    path('end_game/<game_id>', views.end_game, name='end_game'),
    path('how-to-play/', TemplateView.as_view(template_name='presentation/how-to-play.html'), name='instructions'),
    path('controller/<game_id>', views.controller, name='controller'),
]