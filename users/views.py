from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from articles.models import Article


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = request.POST.get('role', 'leitor')
            if role not in ['leitor', 'jornalista']:
                role = 'leitor'
            location = request.POST.get('location', '')
            user.profile.role = role
            user.profile.location = location
            user.profile.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {username}!')
                
                if user.profile.role == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('home')


def journalist_profile(request, username):
    if request.user.is_authenticated and (request.user.profile.role == 'admin' or request.user.is_superuser):
        return redirect('admin_dashboard')
    
    user = get_object_or_404(User, username=username)
    articles = Article.objects.filter(author=user, published=True, approval_status='approved').order_by('-created_at')
    
    context = {
        'profile_user': user,
        'articles': articles,
        'total_posts': articles.count(),
    }
    return render(request, 'users/journalist_profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        profile = user.profile
        
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        profile.bio = request.POST.get('bio', '')
        profile.location = request.POST.get('location', '')
        
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        if 'banner' in request.FILES:
            profile.banner = request.FILES['banner']
        
        user.save()
        profile.save()
        
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('journalist_profile', username=user.username)
    
    return render(request, 'users/edit_profile.html')
