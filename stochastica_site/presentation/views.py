from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect
from django.utils.timezone import now

from .models import get_next_image, get_image_at_index, Game

from string import ascii_uppercase
from random import choices


def home(request):
    if isinstance(request.user, AnonymousUser):
        return redirect('/login/')

    game_id = ''.join(choices(ascii_uppercase, k=5))
    return render(request, 'index.html', context={
        'game_id': game_id
    })

def slide(request, game_id):
    """
    index = 1   => get new random slide
    index = 0   => last viewed slide
    index < 0   => previously viewed slides
    """
    if not request.user.is_authenticated:
        return redirect('/')
    index = request.GET.get('index')
    if index is not None:
        index = int(index)
        game = Game.objects.filter(user=request.user).order_by('-start_time').first()
    else:
        index = 1
        game = Game(user=request.user)
        game.save()

    elapsed_time = now() - game.start_time
    seconds = elapsed_time.seconds
    time_left = game.time_limit - seconds

    if index <= 0:
        image = get_image_at_index(request.user, index)
    else:
        image = get_next_image(request.user)
    return render(request, 'presentation/index.html', context={
        'image': image.image.url,
        'next': min(1, index + 1),
        'prev': min(-1, index - 1),
        'elapsed_time': time_left,
        'game_id': game_id
    })

def controller(request):
    return render(request, 'presentation/controller.html')

def next_round(request, game_id):
    if isinstance(request.user, AnonymousUser):
        return redirect('/login/')
    game = Game.objects.filter(user=request.user).order_by('-start_time').first()
    game.end_time = now()
    game.save()
    return render(request, 'presentation/next_round.html', context={
        'game_id': game_id
    })

def end_game(request, game_id):
    if isinstance(request.user, AnonymousUser):
        return redirect('/login/')
    return render(request, 'index.html', context={
        'game_id': game_id
    })
