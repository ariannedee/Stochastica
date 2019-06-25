from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from django.forms import Form, CharField
from django.shortcuts import render, redirect
from django.utils.timezone import now

from .models import get_next_image, get_image_at_index, Game, generate_game_id


class GameForm(Form):
    game_id = CharField(max_length=5)

    def clean(self):
        try:
            Game.objects.get(game_id=self.cleaned_data['game_id'])
        except Game.DoesNotExist:
            raise ValidationError({'game_id': 'This doesn\'t match an active game'})


def controller(request):
    game_id = None
    game_action = 'start game'
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game_id = request.POST['game_id']
            game = Game.objects.get(game_id=game_id)
            if game.round_start_time:
                game_action = 'end game'
    else:
        form = GameForm()

    return render(request, 'presentation/controller.html', {
        'form': form,
        'game_id': game_id,
        'game_action': game_action
    })


def home(request):
    if isinstance(request.user, AnonymousUser):
        return redirect('/login/')

    return render(request, 'index.html', context={
        'game_id': generate_game_id()
    })


def slide(request, game_id):
    """
    index = 1   => get new random slide
    index = 0   => last viewed slide
    index < 0   => previously viewed slides
    """
    if not request.user.is_authenticated:
        return redirect('/')
    try:
        game = Game.objects.get(game_id=game_id)
    except Game.DoesNotExist:
        return redirect('/')
    index = request.GET.get('index')
    if index is not None:
        index = int(index)
    else:
        index = 1
    if game.round_start_time is None:
        game.round_start_time = now()
        game.save()
    elapsed_time = now() - game.round_start_time
    seconds = elapsed_time.seconds
    time_left = game.time_limit - seconds

    if index <= 0:
        image = get_image_at_index(game, index)
    else:
        image = get_next_image(game)
    return render(request, 'presentation/index.html', context={
        'image': image.image.url,
        'next': min(1, index + 1),
        'prev': min(-1, index - 1),
        'elapsed_time': time_left,
        'game_id': game_id
    })


def next_round(request, game_id):
    if isinstance(request.user, AnonymousUser):
        return redirect('/login/')

    game, created = Game.objects.get_or_create(user=request.user, game_id=game_id)
    game.round_start_time = None
    game.save()
    return render(request, 'presentation/next_round.html', context={
        'game_id': game_id
    })


def end_game(request, game_id):
    if isinstance(request.user, AnonymousUser):
        return redirect('/login/')
    game = Game.objects.get(game_id=game_id)
    game.end_time = now()
    game.save()
    return render(request, 'index.html', context={
        'game_id': generate_game_id()
    })
