from django.urls import path
from . import views
app_name = 'account'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('<slug:profile_slug>/', views.profile, name='user_profile'),
    path('<slug:profile_slug>/edit', views.EditProfile.as_view(), name='user_profile_edit'),
    path('subscribe/<int:subscriber_id>/<int:user_id>', views.subscribe, name='subscribe'),
    path('unsubscribe/<int:subscriber_id>/<int:user_id>', views.unsubscribe, name='unsubscribe'),
]
