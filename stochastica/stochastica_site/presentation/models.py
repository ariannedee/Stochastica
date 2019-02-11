from django.db import models
from django.contrib.auth.models import User


class Pack(models.Model):
    name = models.CharField(max_length=200)
    size = models.IntegerField(default=100)
    subscribers = models.ManyToManyField(User, related_name='subscribed_to')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(max_length=300)
    pack = models.ForeignKey(Pack, related_name='images', on_delete=models.SET_NULL, blank=True, null=True)
    viewed_by = models.ManyToManyField(User, related_name='images_viewed', through='ImageView')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def view(self, user):
        view, created = self.views.get_or_create(user=user)
        view.save()
        view.view()


class ImageView(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.name}, {self.image.title}'

    def view(self):
        self.count += 1
        self.save()


def get_next_image(user):
    import random
    images = user.subscribed_to.first().images.all()
    image = images[random.randint(0, images.count() - 1)]
    image.view(user)
    return image


# Do we need to add attributes to the User class here? i.e. number of games played
def bulk_add_images():
    from django.core.files import File
    from django.core.files.temp import NamedTemporaryFile
    import urllib2
    from pathlib import Path

    home = str(Path.home())
    path = Path('Stochastica/stochastica/')
    file = home / path / 'links list.csv'

    print(home)

    imgs = file.read_text().split('\n')

    for i in imgs:
        if Image.objects.filter(title=i):
            pass
        else:
            content = NamedTemporaryFile(delete=True)
            content.write(urllib2.urlopen(i).read())
            content.flush()
            i_add = Image(title=i, image=content)
            i_add.save()
            break
