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
    image = models.ImageField(upload_to='pack_images', max_length=300)
    pack = models.ForeignKey(Pack, related_name='images', on_delete=models.SET_NULL, blank=True, null=True)
    viewed_by = models.ManyToManyField(User, related_name='images_viewed')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# Do we need to add attributes to the User class here? i.e. number of games played
