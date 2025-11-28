from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm, ProfileEditForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from posts.models import Post


# Create your views here.
def home(request):
    messages.get_messages(request)
    # Fetch all posts, ordered by creation date
    posts = Post.objects.all()
    return render(request, 'core/home.html', {'posts': posts})


@login_required
def profile_view(request):
    return render(request, 'account/profile.html', {'user': request.user})

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
            # Get the user and authenticate them
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log the user in
                auth_login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('home')  # Redirect to home or dashboard
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()

    messages.get_messages(request)
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