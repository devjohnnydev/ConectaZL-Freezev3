from rest_framework import viewsets, filters
from articles.models import Article
from comments.models import Comment
from .serializers import ArticleSerializer, CommentSerializer
from .permissions import IsAuthorOrAdminOrReadOnly, IsJournalistOrAdminForCreate


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(published=True)
    serializer_class = ArticleSerializer
    permission_classes = [IsJournalistOrAdminForCreate, IsAuthorOrAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'tags__name']
    ordering_fields = ['created_at', 'views', 'title']
    lookup_field = 'slug'
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(approved=True)
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, approved=False)
