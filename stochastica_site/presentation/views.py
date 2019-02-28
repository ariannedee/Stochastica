from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect
from .models import get_next_image, get_image_at_index


def home(request):
    if isinstance(request.user, AnonymousUser):
        return render(request, 'not_logged_in.html')
    return render(request, 'index.html')


def slide(request):
    if not request.user.is_authenticated:
        return redirect('/')
    index = int(request.GET.get('index', 0))
    if index and index < 0:
        image = get_image_at_index(request.user, index)
    else:
        image = get_next_image(request.user)
    return render(request, 'presentation/index.html', context={
        'image': image.image.url,
        'next': min(0, index + 1),
        'prev': index - 1
    })
