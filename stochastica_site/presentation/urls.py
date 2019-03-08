from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('play/', views.slide, name='slide'),
    path('end_game/', views.end_game, name='end_game'),
    path('how-to-play/', TemplateView.as_view(template_name='presentation/how-to-play.html'), name='instructions'),
]