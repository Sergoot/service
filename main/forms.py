from django import forms
from django.forms import Select

from .models import Training, Exercise


# class TrainingForm(forms.Form):
#     def __init__(self, user, *args, **kwargs):
#         super(TrainingForm, self).__init__(*args, **kwargs)
#
#         if user.is_authenticated:
#             private_choices = Exercise.objects.filter(user=user)[:5]
#             public_choices = Exercise.objects.all()
#             self.fields['title'] = forms.CharField(label='Название')
#             self.fields['private_exercises'] = forms.ModelMultipleChoiceField(queryset=private_choices,
#                                                                               required=False,
#                                                                               widget=forms.CheckboxSelectMultiple(),
#                                                                               )
#             self.fields['public_exercises'] = forms.ModelMultipleChoiceField(queryset=public_choices,
#                                                                              widget=forms.CheckboxSelectMultiple(),
#                                                                              required=False)
class TrainingForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        private_choices = Exercise.objects.filter(user=user, is_private=True)
        self.fields['private_exercises'] = forms.ModelMultipleChoiceField(queryset=private_choices,
                                                                          required=False,
                                                                          widget=forms.CheckboxSelectMultiple(),)

    public_choices = Exercise.objects.all()
    public_exercises = forms.ModelMultipleChoiceField(queryset=public_choices,widget=forms.CheckboxSelectMultiple(),required=False,)
    title = forms.CharField()


class ExerciseForm(forms.ModelForm):
    is_private = forms.BooleanField(required=False)

    class Meta:
        model = Exercise
        fields = ('title', 'weight', 'approaches', 'repetition', 'muscle_category', 'is_private')



