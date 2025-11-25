from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.text import slugify
from django.db import models
from .models import Article, Like
from comments.models import Comment
import folium


def home(request):
    articles_list = Article.objects.filter(published=True, approval_status='approved')
    featured_articles = Article.objects.filter(published=True, approval_status='approved', featured=True)[:3]
    
    paginator = Paginator(articles_list, 9)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    
    return render(request, 'articles/home.html', {
        'articles': articles,
        'featured_articles': featured_articles
    })


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    
    is_author = request.user.is_authenticated and article.author == request.user
    is_admin = request.user.is_authenticated and request.user.profile.role == 'admin'
    is_public = article.published and article.approval_status == 'approved'
    
    if not (is_public or is_author or is_admin):
        if not article.published:
            messages.error(request, 'Este artigo não está publicado.')
        elif article.approval_status != 'approved':
            messages.error(request, 'Este artigo ainda não foi aprovado.')
        else:
            messages.error(request, 'Você não tem permissão para ver este artigo.')
        return redirect('home')
    
    if is_public:
        article.increment_views()
    
    comments = article.comments.filter(approved=True)
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = article.likes.filter(user=request.user).exists()
    
    map_html = None
    if article.latitude and article.longitude:
        m = folium.Map(location=[article.latitude, article.longitude], zoom_start=13)
        folium.Marker(
            [article.latitude, article.longitude],
            popup=article.location_name or article.title,
            tooltip=article.location_name
        ).add_to(m)
        map_html = m._repr_html_()
    
    return render(request, 'articles/article_detail.html', {
        'article': article,
        'comments': comments,
        'user_has_liked': user_has_liked,
        'map_html': map_html
    })


@login_required
def article_create(request):
    if request.user.profile.role not in ['jornalista', 'admin']:
        messages.error(request, 'Apenas jornalistas podem criar artigos.')
        return redirect('home')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        excerpt = request.POST.get('excerpt', '')
        image = request.FILES.get('image')
        published = request.POST.get('published') == 'on'
        featured = request.POST.get('featured') == 'on'
        tags = request.POST.get('tags', '')
        
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        location_name = request.POST.get('location_name', '')
        
        slug = slugify(title)
        base_slug = slug
        counter = 1
        while Article.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        
        if request.user.profile.role == 'admin':
            approval_status = 'approved'
            from django.utils import timezone
            approved_by = request.user
            approved_at = timezone.now()
        else:
            approval_status = 'pending'
            approved_by = None
            approved_at = None
        
        article = Article.objects.create(
            title=title,
            slug=slug,
            content=content,
            excerpt=excerpt,
            image=image,
            author=request.user,
            published=published,
            featured=featured,
            approval_status=approval_status,
            approved_by=approved_by,
            approved_at=approved_at,
            latitude=float(latitude) if latitude else None,
            longitude=float(longitude) if longitude else None,
            location_name=location_name
        )
        
        if tags:
            article.tags.add(*[tag.strip() for tag in tags.split(',')])
        
        if approval_status == 'pending':
            messages.success(request, 'Artigo criado! Aguardando aprovação do administrador.')
        else:
            messages.success(request, 'Artigo criado e aprovado com sucesso!')
        return redirect('article_detail', slug=article.slug)
    
    return render(request, 'articles/article_form.html')


@login_required
def article_edit(request, slug):
    article = get_object_or_404(Article, slug=slug)
    
    if article.author != request.user and request.user.profile.role != 'admin':
        messages.error(request, 'Você não tem permissão para editar este artigo.')
        return redirect('article_detail', slug=slug)
    
    if request.method == 'POST':
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.excerpt = request.POST.get('excerpt', '')
        article.published = request.POST.get('published') == 'on'
        article.featured = request.POST.get('featured') == 'on'
        
        if request.FILES.get('image'):
            article.image = request.FILES.get('image')
        
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        article.latitude = float(latitude) if latitude else None
        article.longitude = float(longitude) if longitude else None
        article.location_name = request.POST.get('location_name', '')
        
        new_slug = slugify(article.title)
        if new_slug != article.slug:
            base_slug = new_slug
            counter = 1
            while Article.objects.filter(slug=new_slug).exclude(id=article.id).exists():
                new_slug = f'{base_slug}-{counter}'
                counter += 1
            article.slug = new_slug
        article.save()
        
        tags = request.POST.get('tags', '')
        if tags:
            article.tags.clear()
            article.tags.add(*[tag.strip() for tag in tags.split(',')])
        
        messages.success(request, 'Artigo atualizado com sucesso!')
        return redirect('article_detail', slug=article.slug)
    
    return render(request, 'articles/article_form.html', {'article': article})


@login_required
def article_delete(request, slug):
    article = get_object_or_404(Article, slug=slug)
    
    if article.author != request.user and request.user.profile.role != 'admin':
        messages.error(request, 'Você não tem permissão para deletar este artigo.')
        return redirect('article_detail', slug=slug)
    
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Artigo deletado com sucesso!')
        return redirect('home')
    
    return render(request, 'articles/article_confirm_delete.html', {'article': article})


@login_required
def toggle_like(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    like, created = Like.objects.get_or_create(user=request.user, article=article)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'total_likes': article.total_likes()
    })


def highlights_page(request):
    from django.db.models import Count
    
    featured_articles = Article.objects.filter(
        published=True, 
        approval_status='approved', 
        featured=True
    ).order_by('-created_at')
    
    most_liked = Article.objects.filter(
        published=True, 
        approval_status='approved'
    ).annotate(
        likes_count=Count('likes')
    ).filter(likes_count__gt=0).order_by('-likes_count')[:6]
    
    most_commented = Article.objects.filter(
        published=True, 
        approval_status='approved'
    ).annotate(
        comments_count=Count('comments', filter=models.Q(comments__approved=True))
    ).filter(comments_count__gt=0).order_by('-comments_count')[:6]
    
    return render(request, 'articles/highlights.html', {
        'featured_articles': featured_articles,
        'most_liked': most_liked,
        'most_commented': most_commented
    })


def news_feed(request):
    articles_list = Article.objects.filter(
        published=True, 
        approval_status='approved'
    ).select_related('author', 'author__profile').order_by('-created_at')
    
    paginator = Paginator(articles_list, 10)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    
    return render(request, 'articles/news_feed.html', {
        'articles': articles
    })


def journalist_profile(request, username):
    from django.contrib.auth.models import User
    
    if request.user.is_authenticated and (request.user.profile.role == 'admin' or request.user.is_superuser):
        return redirect('admin_dashboard')
    
    journalist = get_object_or_404(User, username=username)
    
    user_articles = Article.objects.filter(
        author=journalist,
        published=True,
        approval_status='approved'
    ).order_by('-created_at')
    
    total_likes = sum(article.total_likes() for article in user_articles)
    total_views = sum(article.views for article in user_articles)
    
    return render(request, 'articles/journalist_profile.html', {
        'journalist': journalist,
        'articles': user_articles,
        'total_articles': user_articles.count(),
        'total_likes': total_likes,
        'total_views': total_views
    })
