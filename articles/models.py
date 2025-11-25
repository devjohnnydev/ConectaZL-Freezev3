from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class Article(models.Model):
    APPROVAL_STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
    ]
    
    title = models.CharField(max_length=255, verbose_name='Título')
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField(verbose_name='Conteúdo')
    excerpt = models.TextField(max_length=500, verbose_name='Resumo', blank=True)
    image = models.ImageField(upload_to='articles/', verbose_name='Imagem', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name='Autor')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    published = models.BooleanField(default=False, verbose_name='Publicado')
    views = models.PositiveIntegerField(default=0, verbose_name='Visualizações')
    featured = models.BooleanField(default=False, verbose_name='Destaque')
    
    approval_status = models.CharField(
        max_length=20, 
        choices=APPROVAL_STATUS_CHOICES, 
        default='pending',
        verbose_name='Status de Aprovação'
    )
    approval_notes = models.TextField(blank=True, verbose_name='Notas de Aprovação')
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='approved_articles',
        verbose_name='Aprovado por'
    )
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name='Aprovado em')
    
    tags = TaggableManager(verbose_name='Tags', blank=True)
    
    latitude = models.FloatField(null=True, blank=True, verbose_name='Latitude')
    longitude = models.FloatField(null=True, blank=True, verbose_name='Longitude')
    location_name = models.CharField(max_length=255, blank=True, verbose_name='Nome do Local')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Artigo'
        verbose_name_plural = 'Artigos'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    def total_likes(self):
        return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name='Usuário')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes', verbose_name='Artigo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Curtido em')
    
    class Meta:
        unique_together = ('user', 'article')
        verbose_name = 'Curtida'
        verbose_name_plural = 'Curtidas'
    
    def __str__(self):
        return f'{self.user.username} curtiu {self.article.title}'
