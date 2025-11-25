from rest_framework import serializers
from articles.models import Article
from comments.models import Comment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags_list = serializers.SerializerMethodField()
    total_likes = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'content', 'excerpt', 'image', 'author', 
                  'created_at', 'updated_at', 'published', 'views', 'featured', 
                  'tags_list', 'latitude', 'longitude', 'location_name', 'total_likes']
        read_only_fields = ['slug', 'created_at', 'updated_at', 'views']
    
    def get_tags_list(self, obj):
        return [tag.name for tag in obj.tags.all()]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    article_title = serializers.CharField(source='article.title', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'article', 'article_title', 'user', 'content', 'created_at', 'updated_at', 'approved']
        read_only_fields = ['created_at', 'updated_at', 'approved']
