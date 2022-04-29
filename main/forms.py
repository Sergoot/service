from django import forms
from django.forms import Select

from .models import Training, Exercise


class TrainingForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        if user.is_authenticated:
            choices = Exercise.objects.filter(user=user)[:5]
            self.fields['title'] = forms.CharField(label='Название')
            self.fields['exercises'] = forms.ModelMultipleChoiceField(queryset=choices, widget=forms.CheckboxSelectMultiple)


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('title',)
