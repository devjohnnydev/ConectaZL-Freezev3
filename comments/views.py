from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Comment
from articles.models import Article


@login_required
def add_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                article=article,
                user=request.user,
                content=content,
                approved=False
            )
            messages.success(request, 'Comentário enviado! Aguardando aprovação.')
        else:
            messages.error(request, 'O comentário não pode estar vazio.')
    
    return redirect('article_detail', slug=article.slug)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.user != request.user and request.user.profile.role != 'admin':
        messages.error(request, 'Você não tem permissão para deletar este comentário.')
        return redirect('article_detail', slug=comment.article.slug)
    
    article_slug = comment.article.slug
    comment.delete()
    messages.success(request, 'Comentário deletado!')
    return redirect('article_detail', slug=article_slug)
