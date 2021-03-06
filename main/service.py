from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from main.models import Training, Like


def get_subscriptions(request) -> list:
    """ Получает тренировки из подписок """
    all_trains = []
    for subscription in request.user.subscriptions.all():
        sub_user_trainings = Training.objects.filter(user=subscription.user).order_by('-pub_date')
        for training in sub_user_trainings:
            all_trains.append(training)
    return all_trains


def add_like(obj, user):
    """ Добавляет лайк к obj. """
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(content_type=obj_type,
                                                  object_id=obj.id,
                                                  user=user)
    return like


def remove_like(obj, user):
    """ Удаляет лайк с obj. """
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(content_type=obj_type,
                        object_id=obj.id,
                        user=user).delete()


def is_fan(obj, user) -> bool:
    """ Проверяет, лайкнул ли user obj. """
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user)
    return likes.exists()


def get_fans(obj):
    """ Получает всех пользователей, которые лайкнули obj."""
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(likes__content_type=obj_type,
                               likes__object_id=obj.id)
