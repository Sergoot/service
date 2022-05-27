from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from account.service import get_exercises
from .forms import TrainingForm, ExerciseForm, CommentForm
from .models import Exercise, Training, UserExercises, Comment
# from .forms import TrainingForm
from .service import get_subscriptions, add_like, remove_like, is_fan


# Create your views here.


def main(request):
    request.session['from_ex'] = False
    context = {'training': get_subscriptions(request)}
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
        user_exs = UserExercises.objects.get(user=self.request.user)
        user_exs.exercises.add(self.object)
        user_exs.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return redirect('/')


def exercise_favorites(request, ex_id):
    exercise = Exercise.objects.get(pk=ex_id)
    user_favorites = UserExercises.objects.get(user=request.user)
    if exercise in user_favorites.exercises.all():
        user_favorites.exercises.remove(exercise)
        return JsonResponse({'response': '&#9734;'})
    else:
        user_favorites.exercises.add(exercise)
        user_favorites.save()
        return JsonResponse({'response': '&#9733;'})

    # return redirect('account:user_profile', request.user.username)


class DetailTraining(DetailView):
    model = Training
    context_object_name = 'training'
    template_name = 'main/training_detail.html'
    pk_url_kwarg = 'train_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        like_content = 'Лайк'
        if is_fan(self.object,self.request.user):
            like_content = 'АнЛайк'
        context['comment_form'] = CommentForm
        context['like_content'] = like_content
        return context


# def exercise_edit(request, ex_id):
#     editing_exercise = Exercise.objects.get(pk=ex_id)
#     if request.method == 'GET':
#         exercise_form = ExerciseForm(instance=editing_exercise)
#         return JsonResponse({'exercise_form': str(exercise_form)}, safe=False)
#     else:
#         exercise_form = ExerciseForm(request.POST)
#         if exercise_form.is_valid():
#             exercise = exercise_form.save(commit=False)
#             exercise.save()
#             user_favorites = UserExercises.objects.get(user=request.user)  # СИЛЬНО ОПТИМИЗИРОВАТЬ!!!!
#             user_favorites.exercises.remove(editing_exercise)
#             request.user.favorite_exercises.get().exercises.add(exercise)
#             request.user.favorite_exercises.get().save()
#             print(exercise)
#         return JsonResponse({'exercise_form': str(exercise_form)},safe=False)


class EditExercise(UpdateView):
    model = Exercise
    pk_url_kwarg = 'ex_id'
    template_name = 'main/exercise_edit.html'
    success_url = 'account:user_profile'
    context_object_name = 'exercise'
    fields = ('title', 'weight', 'approaches', 'repetition', 'muscle_category')

    def form_valid(self, form):
        self.request.session['from_ex'] = True
        if self.object.is_private == False:
            print('FALSE')
            print('self', self.object)                                            # Сделать так, чтобы значение изменялось только в favorites
            self.request.user.favorite_exercises.get().exercises.add(self.object.save())
            self.request.user.favorite_exercises.get().save()
            return redirect(self.success_url, self.request.user.username)
        else:
            print('TRUE')
            self.object = form.save()
            self.object.save()
            return redirect(self.success_url, self.request.user.username)


def like(request, train_id):

    obj = get_object_or_404(Training, pk=train_id)
    if is_fan(obj, request.user):
        remove_like(obj, request.user)
        response = 'Лайк'
    else:
        add_like(obj, request.user)
        response = 'АнЛайк'
    context = {'response': response,
               'total_likes': obj.total_likes()}
    return JsonResponse(context)


@require_POST
def add_comment(request, train_id):
    training = get_object_or_404(Training, pk=train_id)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.training = training
        new_comment.user = request.user
        new_comment.save()
        return JsonResponse(
            {"text": new_comment.text, 'user': new_comment.user.username}, status=201)
    else:
        return JsonResponse(form.errors.as_data(), safe=False, status=200)
