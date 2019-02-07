from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render


# Create your views here.
def index(request):
    if isinstance(request.user, AnonymousUser):
        return render(request, 'not_logged_in.html')
    image = request.user.subscribed_to.first().images.first()
    return render(request, 'index.html', context={'image': image.image.url})
