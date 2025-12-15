from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Post, Like

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
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Automatically assign the logged-in user
        return super().form_valid(form)

# View to create a comment on a post
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'posts/comment_form.html'

    def form_valid(self, form):
        post_id = self.kwargs['post_id']  # Get post_id from URL
        form.instance.user = self.request.user  # Automatically assign the logged-in user
        form.instance.post = get_object_or_404(Post, id=post_id)  # Get the post by ID
        return super().form_valid(form)

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse_lazy('post_detail', kwargs={'pk': post_id})

def user_profile(request, username):
    # Retrieve the user by their username
    user = get_object_or_404(get_user_model(), username=username)
    
    posts = Post.objects.filter(user=user)

    is_following = False

    if request.user.is_authenticated:
        is_following = user.followers.filter(id=request.user.id).exists()
    
    # Render the user profile page with the user's data and their posts
    return render(request, 'account/profile.html', {
        'user': user,
        'posts': posts,
        'is_following': is_following,
        })


@login_required
@require_POST
def toggle_like(request, post_id):
    """Toggle like for a post"""
    try:
        # Get the post
        post = get_object_or_404(Post, id=post_id)
        
        # Check current like status
        is_liked = post.likes.filter(id=request.user.id).exists()
        
        # Toggle like
        if is_liked:
            # Unlike
            post.likes.remove(request.user)
            liked = False
        else:
            # Like
            post.likes.add(request.user)
            liked = True
        
        # Get updated count
        like_count = post.likes.count()
        
        return JsonResponse({
            'success': True,
            'liked': liked,
            'like_count': like_count
        })
        
    except Post.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Post not found'
        }, status=404)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'An error occurred'
        }, status=500)
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the post object
        post = self.get_object()
        # Get all comments for this post, ordered by creation date
        comments = post.comments.all().order_by('created_at')
        context['comments'] = comments
        # Add comment form to context if you want to display it on the same page
        context['comment_form'] = CommentForm()
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs['pk'])