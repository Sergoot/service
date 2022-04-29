from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView

from account import views as accviews
from account.models import Profile
from .models import Exercise, Training
# from .forms import TrainingForm
# Create your views here.


def main(request):
    all_trains = []
    for subscription in request.user.subscriptions.all():
        sub_user_trainings = Training.objects.filter(user=subscription.user).order_by('-pub_date')
        for training in sub_user_trainings:
            all_trains.append(training)
    context = {'training': all_trains}
    print(all_trains)
    return render(request, 'main/main.html', context)


def new_train(request):
    train_title = request.POST['title']
    train_exs = request.POST.getlist('exercises')
    new_training = Training.objects.create(
        title=train_title,
        user=request.user,
    )
    for ex in train_exs:
        new_training.exercises.add(ex)
        new_training.save()
    return redirect('account:user_profile', request.user.username)


def delete_train(request, train_id):
    train = Training.objects.get(pk=train_id)
    train.delete()
    return redirect('account:user_profile', request.user.username)


class ExerciseCreate(CreateView):
    model = Exercise
    fields = ['title','weight', 'approaches', 'repetition','muscle_category']
    context_object_name = 'exercise_form'
