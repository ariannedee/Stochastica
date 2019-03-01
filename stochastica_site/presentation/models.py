from django.db import models
from django.contrib.auth.models import User


class Pack(models.Model):
    name = models.CharField(max_length=200)
    size = models.IntegerField(default=100)
    subscribers = models.ManyToManyField(User, related_name='subscribed_to', blank=True, null=True)
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
        return f'{self.user.username}: {self.image.title}'

    def view(self):
        self.count += 1
        self.save()


def get_next_image(user):
    import random
    images = Image.objects.filter(pack__subscribers=user)
    images = images.order_by('views__viewed_at').all()
    image = images[random.randint(0, min(10, images.count() - 1))]
    image.view(user)
    return image


# Takes a negative or 0 index to get previously viewed images
def get_image_at_index(user, index):
    images = Image.objects.filter(pack__subscribers=user)
    # Since QuerySets don't support negative indexing
    # we reverse the order and index by the absolute value
    images = images.order_by('-views__viewed_at').all()
    max_index = images.count() - 1
    image = images[min(abs(index), max_index)]
    return image
