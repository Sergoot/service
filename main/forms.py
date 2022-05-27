from django import forms
from django.forms import Select, models, MultipleChoiceField, Textarea

from .models import Training, Exercise, UserExercises, Comment


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


class CustomModelChoiceIterator(models.ModelChoiceIterator):
    def choice(self, obj):
        return (self.field.prepare_value(obj),
                self.field.label_from_instance(obj), obj)


class CustomModelChoiceField(models.ModelMultipleChoiceField):
    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return CustomModelChoiceIterator(self)
    choices = property(_get_choices, MultipleChoiceField._set_choices)


class TrainingForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        private_choices = UserExercises.objects.get(user=user).exercises.all()
        # private_choices = Exercise.objects.all()
        # Добавить ограничение по количеству
        print(private_choices)
        self.fields['private_exercises'] = CustomModelChoiceField(queryset=private_choices,
                                                                  required=False,
                                                                  widget=forms.CheckboxSelectMultiple())
    public_choices = Exercise.objects.filter(is_private=False).order_by('-popularity') # Добавить ограничение по количеству
    public_exercises = CustomModelChoiceField(queryset=public_choices,
                                              widget=forms.CheckboxSelectMultiple(),
                                              required=False)
    title = forms.CharField()


class ExerciseForm(forms.ModelForm):
    is_private = forms.BooleanField(required=False)

    class Meta:
        model = Exercise
        fields = ('title', 'weight', 'approaches', 'repetition', 'muscle_category', 'is_private')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {'text': Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваш комментарий',
                'id': 'inputPassword5',
                'aria-describedby': 'passwordHelpBlock',
            }
        )}

