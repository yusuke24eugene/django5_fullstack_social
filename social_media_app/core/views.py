from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileEditForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate, get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from posts.models import Post
from django.shortcuts import get_object_or_404

User = get_user_model()

# Create your views here.
def home(request):
    messages.get_messages(request)
    # Fetch all posts, ordered by creation date
    posts = Post.objects.all()
    return render(request, 'core/home.html', {'posts': posts})

@login_required
def profile_view(request):

    user_posts = Post.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'account/profile.html', {
        'user': request.user,
        'posts': user_posts,
    })

@login_required
def profile_edit_view(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after successful update
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'account/profile_edit.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Get the user from cleaned_data
            user = form.cleaned_data.get('user')
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        # If form is invalid, errors are already attached to form
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Make sure the group exists before adding the user to it
            try:
                group = Group.objects.get(name='User')  # Ensure this group exists in your database
                user.groups.add(group)
            except Group.DoesNotExist:
                print("Group 'User' does not exist.")
                # Optionally create the group
                group = Group.objects.create(name='User')
                user.groups.add(group)

            # Automatically log the user in after registration
            auth_login(request, user)
            messages.success(request, 'Account successfully created!')
            return redirect('home')  # Redirect to a success page or home page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'account/register.html', {'form': form})

def logout(request):
    auth_logout(request)  # This logs the user out and clears the session
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')  # Redirect to the home page or any other page

@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        return redirect('profile', username=username)

    if target_user.followers.filter(id=request.user.id).exists():
        target_user.followers.remove(request.user)
    else:
        target_user.followers.add(request.user)

    return redirect('user_profile', username=username)