from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('profile', views.profile_view, name='profile'),
    path('edit-profile', views.profile_edit_view, name='profile_edit'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]