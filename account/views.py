from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.generic import UpdateView
from main.models import Exercise, Training, UserExercises
from .forms import LoginForm, UserRegistrationForm, ProfileEdit
from django.contrib.auth import logout
from main import views as vmain
from .models import Profile
from .tasks import send_greetings_email
from .service import get_profile_context, create_exercise_form_save, get_all_or_filter


def logout_view(request):
    """ Выход пользователя из сессии """
    logout(request)
    return redirect(vmain.main)


def user_login(request):
    """ Вход пользователя  """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(vmain.main)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    """ Регистрация пользователя """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            # send_greetings_email.delay(new_user.email)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            user_exs = UserExercises()
            user_exs.user = new_user
            user_exs.save()
            profile = Profile()
            profile.user = new_user
            profile.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/1index.html', {'user_form': user_form})


def profile(request, profile_slug):
    """ Вью для профиля пользователя """
    context = get_profile_context(request, profile_slug)

    if request.method == 'POST':
        create_exercise_form_save(request.POST)
        return render(request, 'account/user_profile.html', context)

    if request.user.username != profile_slug:
        return render(request, 'account/user_profile_guest.html', context)
    return render(request, 'account/user_profile.html', context)


class EditProfile(UpdateView):
    """ Изменение профиля """
    model = Profile
    template_name = 'account/user_profile_edit.html'
    slug_url_kwarg = 'profile_slug'
    form_class = ProfileEdit

    def get(self, request, *args, **kwargs):
        user_profile = get_object_or_404(self.model, user=request.user)
        user_form = self.form_class(data={
                                          'username': user_profile.user.username,
                                          'email': user_profile.user.email,
                                          'bio': user_profile.bio,
                                         }
                                    )
        user_form.email = request.user.email
        return render(request, self.template_name, {'profile_form': user_form, 'profile': user_profile})

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.refresh_from_db()
        self.object.user.username = form.cleaned_data['username']
        self.object.user.email = form.cleaned_data['email']
        self.object.bio = form.cleaned_data['bio']
        self.object.user.save()
        self.object.save()
        return redirect(f'/account/{self.object.user.username}')


def subscribe(request, subscriber_id, user_id):
    """ Логика подписки на профиль пользователя """
    profile = Profile.objects.get(user=user_id)
    user_profile = User.objects.get(pk=user_id)
    profile.followers.add(subscriber_id)
    profile.save()
    return redirect('account:user_profile', user_profile.username)


def unsubscribe(request, subscriber_id, user_id):
    """ Логика отписки на профль пользователя """
    profile = Profile.objects.get(user=user_id)
    user_profile = User.objects.get(pk=user_id)
    profile.followers.remove(subscriber_id)
    profile.save()
    return redirect('account:user_profile', user_profile.username)
