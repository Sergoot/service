
from django.urls import path
from . import views
from .views import ExerciseCreate


urlpatterns = [
    path('', views.main,),
    path('new-training/', views.training_create, name='new_train'),
    path('delete-training/<int:train_id>', views.TrainingDelete.as_view(), name='delete_train'),
    path('new_exercise', ExerciseCreate.as_view(), name='exercise_create')
]