from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect


def index(request):
    if isinstance(request.user, AnonymousUser):
        return render(request, 'not_logged_in.html')
    return render(request, 'index.html')


def game(request):
    if not request.user.is_authenticated:
        return redirect('/')
    image = request.user.subscribed_to.first().images.first()
    return render(request, 'presentation/index.html', context={'image': image.image.url})
