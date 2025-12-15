from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('profile', views.profile_view, name='profile'),
    path('edit-profile', views.profile_edit_view, name='profile_edit'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)