from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, PostForm
from .models import Post

def home(request):
    # If user is authenticated, redirect to profile
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'core/home.html')

def login(request):
    # Force new session for login page access
    if not request.session.session_key:
        request.session.create()
    
    # If accessing login page, ensure fresh session
    if request.method == "GET":
        auth_logout(request)
        request.session.flush()
        request.session.create()
        form = AuthenticationForm()
        return render(request, 'core/login.html', {'form': form})
        
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Create new session for successful login
            request.session.flush()
            request.session.create()
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('profile')
    else:
        form = AuthenticationForm()
        
    return render(request, 'core/login.html', {'form': form})

def register(request):
    # If user is already authenticated, redirect to profile
    if request.user.is_authenticated:
        return redirect('profile')
        
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
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been created!')
            return redirect('profile')
    else:
        form = PostForm()
    
    user_posts = Post.objects.filter(author=request.user).order_by('-date_posted')
    context = {
        'user': request.user,
        'form': form,
        'posts': user_posts
    }
    return render(request, 'core/profile.html', context)

def logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')
