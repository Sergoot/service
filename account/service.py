from django.core.mail import send_mail
from django.conf import settings
from django.db.models.base import Model
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from account.models import Profile
from main.forms import TrainingForm, ExerciseForm, CommentForm
from main.models import Training


def mail(email: str) -> None:
    """ Отправляет приветственный email """
    subject = 'Спасибо за регистрацию!!'
    message = ' Добро пожаловать в Muscles Service '
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email], fail_silently=False)


def get_profile_context(request, profile_slug: str):
    """ Вовзращает контекст для профиля """
    print(type(request))
    print(type(profile_slug))
    profile = get_object_or_404(Profile, slug=profile_slug)
    trainings = Training.objects.filter(user=request.user).order_by('-pub_date')[:5]
    training_form = TrainingForm(user=request.user)
    create_exercise_form = ExerciseForm
    if request.user.username != profile_slug:
        context = {'profile': profile}
    else:
        context = {
            'profile': profile,
            'training_form': training_form,
            'exercise_form': create_exercise_form,
            'trainings': trainings,
            'from_ex': request.session['from_ex'],
            }
    return context


def get_all_or_filter(model: Model, **filters: any) -> QuerySet:
    """ Возвращает QuerySet со всеми атрибутами модели или отфильтрованными по фильтрам атрибутами """
    return model.objects.filter(**filters) if filters else model.objects.all()


def create_exercise_form_save(request_post) -> None:
    """ Создает ExerciseForm """
    create_exercise_form = ExerciseForm(request_post)
    if create_exercise_form.is_valid():
        create_exercise_form.save()


def get_exercises(request, cleaned_data) -> None:
    """ Получает упражнения в зависимости от содержимого cleaned_data """
    new_training = Training.objects.create(
            title=cleaned_data['title'],
            user=request.user,
        )
    if cleaned_data['private_exercises']:
        for ex in cleaned_data['private_exercises']:
            ex.popularity += 1
            ex.save()
            new_training.exercises.add(ex)
    if cleaned_data['public_exercises']:
        for ex in cleaned_data['public_exercises']:
            ex.popularity += 1
            ex.save()
            new_training.exercises.add(ex)
    new_training.save()


