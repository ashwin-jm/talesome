from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import Post
#Adding for deployment

def home(request):
    return render(request, 'core/home.html')

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Auto-login after registration
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!")
            # Create a new empty form instance
            form = UserRegisterForm()
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == "POST":
        messages.info(request, "Post creation feature is under development!")
        return redirect('profile')
    
    user_posts = Post.objects.filter(author=request.user).order_by('-date_posted')
    context = {
        'user': request.user,
        'posts': user_posts
    }
    return render(request, 'core/profile.html', context)

def logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')
