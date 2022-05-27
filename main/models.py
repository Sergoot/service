from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

MUSCLE_CATEGORY_CHOICES = [
    ('грудь', 'грудь'), ('спина', 'спина'), ('ноги', 'ноги'), ('плечи', 'плечи'), ('руки', 'руки')
]


class Exercise(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='exercises')
    title = models.CharField(max_length=255)
    weight = models.SmallIntegerField()
    approaches = models.SmallIntegerField()
    repetition = models.SmallIntegerField()
    muscle_category = models.CharField(choices=MUSCLE_CATEGORY_CHOICES, max_length=255)
    is_private = models.BooleanField('Приватное',)
    popularity = models.BigIntegerField('Популярность', default=0)

    def __str__(self) -> str:
        return f'{self.title} {self.weight}кг - {self.approaches} по {self.repetition}({self.is_private})'


class UserExercises(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_exercises')
    exercises = models.ManyToManyField(Exercise, blank=True, null=True)


class Like(models.Model):
    user = models.ForeignKey(User,
                             related_name='likes',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Training(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField(default=timezone.now)
    user_mark = models.SmallIntegerField(null=True)
    exercises = models.ManyToManyField(Exercise, related_name='trainings', null=True, blank=True)
    likes = GenericRelation(Like, null=True, on_delete=models.CASCADE)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, null=True, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(default=timezone.now)
    text = models.TextField(default='')




