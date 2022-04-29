
from django.urls import path
from . import views


urlpatterns = [
    path('', views.main,),
    path('account/new-training/', views.new_train, name='new_train'),
    path('account/delete-training/<int:train_id>', views.delete_train, name='delete_train'),
]