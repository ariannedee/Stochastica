from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, Case, When, DateTimeField, F, TimeField
import datetime


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


class Game(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(default=None, blank=True, null=True)
    game_duration = models.TimeField(default=datetime.time(minute=2))
    time_limit = models.IntegerField(default=120)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


def get_next_image(user):
    import random
    all_images = Image.objects.filter(pack__subscribers=user)
    # Order by the last time this user saw this image, with unseen images at the top
    all_images = all_images.annotate(
        last_seen_at=Case(
            When(views__user=user, then=F('views__viewed_at')),
            default=None,
            output_field=DateTimeField()
        )).order_by('last_seen_at')
    num_unseen_images = all_images.filter(last_seen_at__isnull=True).count()
    upper_limit = max(num_unseen_images, 20)
    upper_limit = min(upper_limit, all_images.count() - 1)  # In case there are < 20 images
    image = all_images[random.randint(0, upper_limit)]
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
