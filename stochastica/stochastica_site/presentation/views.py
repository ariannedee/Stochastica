from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect
from .models import get_next_image


def index(request):
    if isinstance(request.user, AnonymousUser):
        return render(request, 'not_logged_in.html')
    return render(request, 'index.html')


def game(request):
    if not request.user.is_authenticated:
        return redirect('/')

    image = get_next_image(request.user)
    return render(request, 'presentation/index.html', context={'image': image.image.url})
