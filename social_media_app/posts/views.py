from django.shortcuts import redirect
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy

# Create your views here.
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        # Filter posts by the logged-in user (if posts are user-specific)
        return Post.objects.filter(user=self.request.user)

# View to create a new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user  # Automatically assign the logged-in user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_list')  # Redirect to post list view after creating

# View to create a comment on a post
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'posts/comment_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user  # Automatically assign the logged-in user
        form.instance.post = Post.objects.get(id=self.kwargs['post_id'])  # Get the post by ID
        return super().form_valid(form)

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return redirect('post_detail', pk=post_id)  # Redirect back to the post detail view after creating the comment
