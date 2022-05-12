from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView

from account import views as accviews
from account.models import Profile
from account.service import get_exercises
from .forms import TrainingForm
from .models import Exercise, Training
# from .forms import TrainingForm
from .service import get_subcriptions
# Create your views here.


def main(request):
    context = {'training': get_subcriptions(request)}
    return render(request, 'main/main.html', context)


def training_create(request):
    form = TrainingForm(user=request.user, data=request.POST)
    print(request.POST)
    if form.is_valid():
        get_exercises(request, form.cleaned_data)
        return redirect('account:user_profile', request.user.username)
    else:
        print(form.errors)
        return HttpResponse(form)


# class TrainingCreate(CreateView):
#     model = Training
#     context_object_name = 'form'
#     template_name = 'account/user_profile.html'
#     fields = ['title', 'exercises']
#     success_url = 'account:user_profile'
#
#     def form_valid(self, form):
#         new_training = Training.objects.create(
#                                             title=form.cleaned_data['title'],
#                                             user=self.request.user,
#                                               )
#         print(form.cleaned_data)
#         if form.cleaned_data['private_exercises']:
#             for ex in form.cleaned_data['private_exercises']:
#                 new_training.exercises.add(ex)
#                 new_training.save()
#         if form.cleaned_data['public_exercises']:
#             for ex in form.cleaned_data['public_exercises']:
#                 new_training.exercises.add(ex)
#                 new_training.save()
#         return redirect(self.success_url, self.request.user.username)
#
#     def form_invalid(self, form):
#         print(form.cleaned_data)
#         errors = []
#         for error in form.errors:
#             errors.append(error)
#         return HttpResponse(errors)


class TrainingDelete(View):
    model = Training
    success_url = 'account:user_profile'

    def get(self, request, **kwargs):
        train = get_object_or_404(self.model, pk=kwargs.get('train_id'))
        train.delete()
        return redirect(self.success_url, request.user.username)


class ExerciseCreate(CreateView):
    model = Exercise
    template_name = 'account/user_profile.html'
    fields = ['title', 'weight', 'approaches', 'repetition', 'muscle_category', 'is_private']
    context_object_name = 'exercise_form'

    def get_success_url(self):
        success_url = f'account/{self.request.user.username}'
        return success_url

    def form_valid(self, form):
        print(form.cleaned_data)
        self.object = form.save(commit=False)
        self.object.is_private = form.cleaned_data['is_private']
        self.object.user = self.request.user
        self.object.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return redirect('/')


