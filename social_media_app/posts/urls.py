from django.urls import path
from .views import PostListView, PostCreateView, CommentCreateView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:post_id>/comment/', CommentCreateView.as_view(), name='comment_create'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),
]