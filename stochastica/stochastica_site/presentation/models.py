from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Image(models.Model):
    image_url = models.TextField('image url location')
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    deleted_at = models.DateTimeField()

class Pack(models.Model):
    name = models.CharField('pack name', max_length=200) # optional field, for example, 'Starter Pack'
    size = models.IntegerField(default=100)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    deleted_at = models.DateTimeField()

class PackContents(models.Model):
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.PROTECT)
        # This means each image can only be assigned to one pack, which I think is desired
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    deleted_at = models.DateTimeField()

class SubscribedTo(models.Model):
    user = models.ManyToManyField(User)
    pack = models.ManyToManyField(Pack)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    deleted_at = models.DateTimeField()

class ImageView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField()

# Do we need to add attributes to the User class here? i.e. number of games played
