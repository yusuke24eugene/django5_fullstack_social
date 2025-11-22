from django.urls import path
from .views import PostListView, PostCreateView, CommentCreateView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:post_id>/comment/', CommentCreateView.as_view(), name='comment_create'),
]
