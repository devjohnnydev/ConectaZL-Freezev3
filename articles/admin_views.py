from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils import timezone
from .models import Article, Like
from comments.models import Comment
from datetime import timedelta


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or (request.user.profile.role != 'admin' and not request.user.is_superuser):
            messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta página.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@admin_required
def admin_dashboard(request):
    total_articles = Article.objects.count()
    pending_articles = Article.objects.filter(approval_status='pending').count()
    approved_articles = Article.objects.filter(approval_status='approved').count()
    rejected_articles = Article.objects.filter(approval_status='rejected').count()
    
    total_users = User.objects.count()
    total_comments = Comment.objects.count()
    pending_comments = Comment.objects.filter(approved=False).count()
    total_likes = Like.objects.count()
    
    recent_articles = Article.objects.all()[:10]
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_comments = Comment.objects.order_by('-created_at')[:5]
    
    top_articles = Article.objects.filter(
        approval_status='approved'
    ).order_by('-views')[:5]
    
    users_by_role = User.objects.values(
        'profile__role'
    ).annotate(count=Count('id'))
    
    context = {
        'total_articles': total_articles,
        'pending_articles': pending_articles,
        'approved_articles': approved_articles,
        'rejected_articles': rejected_articles,
        'total_users': total_users,
        'total_comments': total_comments,
        'pending_comments': pending_comments,
        'total_likes': total_likes,
        'recent_articles': recent_articles,
        'recent_users': recent_users,
        'recent_comments': recent_comments,
        'top_articles': top_articles,
        'users_by_role': users_by_role,
    }
    
    return render(request, 'admin/dashboard.html', context)


@login_required
@admin_required
def admin_articles_pending(request):
    pending_articles = Article.objects.filter(
        approval_status='pending'
    ).order_by('-created_at')
    
    return render(request, 'admin/articles_pending.html', {
        'articles': pending_articles
    })


@login_required
@admin_required
def admin_article_approve(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        notes = request.POST.get('notes', '')
        
        if action == 'approve':
            article.approval_status = 'approved'
            article.approved_by = request.user
            article.approved_at = timezone.now()
            article.approval_notes = notes
            article.save()
            messages.success(request, f'Artigo "{article.title}" aprovado com sucesso!')
        elif action == 'reject':
            article.approval_status = 'rejected'
            article.approved_by = request.user
            article.approved_at = timezone.now()
            article.approval_notes = notes
            article.save()
            messages.warning(request, f'Artigo "{article.title}" rejeitado.')
        
        return redirect('admin_articles_pending')
    
    return render(request, 'admin/article_review.html', {
        'article': article
    })


@login_required
@admin_required
def admin_articles_all(request):
    status_filter = request.GET.get('status', '')
    
    articles = Article.objects.all()
    
    if status_filter:
        articles = articles.filter(approval_status=status_filter)
    
    articles = articles.order_by('-created_at')
    
    return render(request, 'admin/articles_all.html', {
        'articles': articles,
        'status_filter': status_filter
    })


@login_required
@admin_required
def admin_comments_pending(request):
    pending_comments = Comment.objects.filter(
        approved=False
    ).order_by('-created_at')
    
    return render(request, 'admin/comments_pending.html', {
        'comments': pending_comments
    })


@login_required
@admin_required
def admin_comment_approve(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            comment.approved = True
            comment.save()
            messages.success(request, 'Comentário aprovado!')
        elif action == 'delete':
            comment.delete()
            messages.warning(request, 'Comentário deletado.')
        
        return redirect('admin_comments_pending')
    
    return render(request, 'admin/comment_review.html', {
        'comment': comment
    })


@login_required
@admin_required
def admin_users_list(request):
    users = User.objects.all().order_by('-date_joined')
    
    return render(request, 'admin/users_list.html', {
        'users': users
    })


@login_required
@admin_required
def admin_user_toggle_role(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        new_role = request.POST.get('role')
        if new_role in ['leitor', 'jornalista', 'admin']:
            user.profile.role = new_role
            user.profile.save()
            messages.success(request, f'Perfil de {user.username} atualizado para {new_role}!')
        
        return redirect('admin_users_list')
    
    return render(request, 'admin/user_edit.html', {
        'user_obj': user
    })
