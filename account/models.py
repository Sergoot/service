from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils.text import slugify


class Profile(models.Model):

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=255, default='')
    followers = models.ManyToManyField(User, related_name='subscriptions', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        else:
            self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return f'/account/{self.slug}'
