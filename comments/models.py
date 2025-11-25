from django.db import models
from django.contrib.auth.models import User
from articles.models import Article


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='Artigo')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Usuário')
    content = models.TextField(verbose_name='Comentário')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    approved = models.BooleanField(default=False, verbose_name='Aprovado')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
    
    def __str__(self):
        return f'Comentário de {self.user.username} em {self.article.title}'
