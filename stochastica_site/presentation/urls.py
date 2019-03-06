from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('play/', views.slide, name='slide'),
    path('', include('django.contrib.auth.urls')),
]