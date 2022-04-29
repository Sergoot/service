from django.contrib.auth.models import User
from django import forms
from django.forms import TextInput, fields_for_model

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'type': 'password',
        'class': 'form-control',
        'id': 'exampleInputPassword1',
    }))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={
        'type': 'password',
        'class': 'form-control',
        'id': 'exampleInputPassword1',
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        widgets = {'username': TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваш комментарий',
            }
        )}
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class ProfileEdit(forms.ModelForm):
    bio = forms.CharField(label='Расскажите о себе', required=False, widget=forms.Textarea())

    class Meta:
        model = Profile
        fields = ('bio',)


class UserEdit(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')





