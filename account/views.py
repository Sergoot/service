from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, UpdateView

from main.forms import TrainingForm
from main.models import Exercise, Training
from .forms import LoginForm, UserRegistrationForm, ProfileEdit, UserEdit
from django.contrib.auth import logout
from main import views as vmain
from .models import Profile


def logout_view(request):
    logout(request)
    return redirect(vmain.main)


def user_login(request):
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
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #создание нового пользователя
            new_user = user_form.save(commit=False)
            #Сохранение пароля
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохранение нового пользователя
            new_user.save()
            #Создание профиля нового пользователя
            profile = Profile()
            profile.user = new_user
            profile.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/1index.html', {'user_form': user_form})


class ShowProfilePageView(DetailView):
    template_name = 'account/user_profile.html'
    model = ''

    def get_context_data(self, *args, **kwargs):
        # context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        return Profile.objects.get(slug=self.kwargs.get('slug'))
        # page_user = get_object_or_404(Profile, slug=self.kwargs['profile_slug'])
        # context['page_user'] = page_user
        # return context


def profile(request, profile_slug):
    profile = get_object_or_404(Profile, slug=profile_slug)
    trainings = Training.objects.filter(user=request.user).order_by('-pub_date')[:5]
    form = TrainingForm(user=request.user)
    if request.user.username != profile_slug:
        return render(request, 'account/user_profile_guest.html', {'profile': profile})
    return render(request, 'account/user_profile.html', {'profile': profile, 'form': form, 'trainings': trainings})


class EditProfile(UpdateView):
    model = Profile
    template_name = 'account/user_profile_edit.html'
    slug_url_kwarg = 'profile_slug'
    form_class = ProfileEdit
    second_form_class = UserEdit

    def get(self, request, *args, **kwargs):
        user_profile = get_object_or_404(Profile, user=request.user)
        profile_form = self.form_class(instance=user_profile)
        user_form = self.second_form_class(instance=request.user)
        return render(request, self.template_name, {'profile_form': profile_form,'user_form':user_form, 'profile': user_profile})


    def form_valid(self, form):
        user_profile = form.save(commit=False)
        user_profile.user.username = self.request.POST['username']
        user_profile.user.email = self.request.POST['email']
        user_profile.user.save()
        user_profile.save()
        return redirect(f'/account/{user_profile}')


def subscribe(request, subscriber_id, user_id):
    profile = Profile.objects.get(user=user_id)
    user_profile = User.objects.get(pk=user_id)
    profile.followers.add(subscriber_id)
    profile.save()
    return redirect('account:user_profile', user_profile.username)


def unsubscribe(request, subscriber_id, user_id):
    profile = Profile.objects.get(user=user_id)
    user_profile = User.objects.get(pk=user_id)
    profile.followers.remove(subscriber_id)
    profile.save()
    return redirect('account:user_profile', user_profile.username)
