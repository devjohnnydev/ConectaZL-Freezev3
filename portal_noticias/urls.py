"""
URL configuration for portal_noticias project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from articles import views as article_views
from articles import admin_views
from users import views as user_views
from comments import views as comment_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    
    path('', article_views.home, name='home'),
    path('destaques/', article_views.highlights_page, name='highlights'),
    path('noticias/', article_views.news_feed, name='news_feed'),
    path('article/create/', article_views.article_create, name='article_create'),
    path('article/<slug:slug>/', article_views.article_detail, name='article_detail'),
    path('article/<slug:slug>/edit/', article_views.article_edit, name='article_edit'),
    path('article/<slug:slug>/delete/', article_views.article_delete, name='article_delete'),
    path('article/<int:article_id>/like/', article_views.toggle_like, name='toggle_like'),
    
    path('comment/<int:article_id>/add/', comment_views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', comment_views.delete_comment, name='delete_comment'),
    
    path('register/', user_views.register_view, name='register'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('profile/edit/', user_views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', user_views.journalist_profile, name='user_profile'),
    
    path('admin-dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/articles/pending/', admin_views.admin_articles_pending, name='admin_articles_pending'),
    path('admin-dashboard/articles/all/', admin_views.admin_articles_all, name='admin_articles_all'),
    path('admin-dashboard/article/<int:article_id>/approve/', admin_views.admin_article_approve, name='admin_article_approve'),
    path('admin-dashboard/comments/pending/', admin_views.admin_comments_pending, name='admin_comments_pending'),
    path('admin-dashboard/comment/<int:comment_id>/approve/', admin_views.admin_comment_approve, name='admin_comment_approve'),
    path('admin-dashboard/users/', admin_views.admin_users_list, name='admin_users_list'),
    path('admin-dashboard/user/<int:user_id>/edit/', admin_views.admin_user_toggle_role, name='admin_user_toggle_role'),
    
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
