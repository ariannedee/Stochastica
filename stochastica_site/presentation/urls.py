from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('play/', views.slide, name='slide'),
    path('next_round/', views.next_round, name='next_round'),
    path('play/next_round/', views.next_round, name='next_round_2'), # Need to fix this, just a dumb js thing
    path('end_game/', views.end_game, name='end_game'),
    path('how-to-play/', TemplateView.as_view(template_name='presentation/how-to-play.html'), name='instructions'),
    path('play/controller/', views.controller, name='controller'),
]