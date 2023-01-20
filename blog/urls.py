from django.urls import path
from django.views.generic.base import RedirectView

from blog import views

app_name = 'blog'

urlpatterns = [
    path('articles/', views.IndexListView.as_view(), name='index'),
    path('', RedirectView.as_view(pattern_name='blog:index', permanent=False)),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('articles/new/', views.ArticleCreateView.as_view(), name='new_article'),
    path('articles/<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='update_article'),
    path('articles/<int:pk>/delete/', views.ArticleDestroyView.as_view(), name='destroy_article'),

    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('blogs/<int:pk>/', views.BlogDetailView.as_view(), name='articles_by_blog'),
    path('blogs/new', views.BlogCreateView.as_view(), name='new_blog'),
]
