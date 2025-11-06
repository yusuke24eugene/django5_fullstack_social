from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import Group

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

def login(request):
    return render(request, 'core/login.html')

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

def logout():
    pass