from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404

from account.models import Profile
from main.forms import TrainingForm, ExerciseForm
from main.models import Training


def mail(email):
    subject = 'Спасибо за регистрацию!!'
    message = ' Всё работает :) '
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email], fail_silently=False)


def get_profile_context(request, profile_slug):
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
            }
    return context


def create_exercise_form_save(request_post):
    create_exercise_form = ExerciseForm(request_post)
    if create_exercise_form.is_valid():
        create_exercise_form.save()


def get_exercises(request, cleaned_data):
    new_training = Training.objects.create(
            title=cleaned_data['title'],
            user=request.user,
        )

    if cleaned_data['private_exercises']:             ##'''МОЖНО КАК ТО СОКРАТИТЬ'''
        for ex in cleaned_data['private_exercises']:
            new_training.exercises.add(ex)
    if cleaned_data['public_exercises']:
        for ex in cleaned_data['public_exercises']:
            new_training.exercises.add(ex)
    new_training.save()



# def subscribe_(user_id, subscriber_id):
#     profile = Profile.objects.get(user=user_id)
#     user_profile = User.objects.get(pk=user_id)
#     profile.followers.add(subscriber_id)
#     profile.save()
#
