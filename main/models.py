from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


MUSCLE_CATEGORY_CHOICES = [
    ('грудь', 'грудь'), ('спина', 'спина'), ('ноги', 'ноги'), ('плечи', 'плечи'), ('руки', 'руки')
]


class Exercise(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    weight = models.SmallIntegerField()
    approaches = models.SmallIntegerField()
    repetition = models.SmallIntegerField()
    muscle_category = models.CharField(choices=MUSCLE_CATEGORY_CHOICES,max_length=255)

    def __str__(self):
        return self.title

    def __int__(self):
        return self.id

class Training(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField(default=timezone.now)
    user_mark = models.SmallIntegerField(null=True)
    exercises = models.ManyToManyField(Exercise, related_name='trainings')


    def __str__(self):
        return self.title



