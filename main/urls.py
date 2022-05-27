
from django.urls import path
from . import views
from .views import ExerciseCreate


urlpatterns = [
    path('', views.main, name='main'),
    path('new-training/', views.training_create, name='new_train'),
    path('delete-training/<int:train_id>', views.TrainingDelete.as_view(), name='delete_train'),
    path('new_exercise', ExerciseCreate.as_view(), name='exercise_create'),
    path('exercise_favorites/<int:ex_id>', views.exercise_favorites, name='exs_favorites'),
    path('training/<int:train_id>', views.DetailTraining.as_view(), name='training_detail'),
    path('exercise_edit/<int:ex_id>', views.EditExercise.as_view(), name='exercise_edit'),
    path('training/<int:train_id>/like', views.like, name='like'),
    path('training/<int:train_id>/comment', views.add_comment, name='comment'),
]
