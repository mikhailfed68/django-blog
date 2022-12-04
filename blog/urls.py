from django.urls import path
from django.views.generic.base import RedirectView

from blog.views import views

app_name = 'blog'

urlpatterns = [
    path('articles/', views.IndexListView.as_view(), name='index'),
    path('', RedirectView.as_view(pattern_name='blog:index', permanent=False)),

    path('articles/new/', views.ArticleFormCreateView.as_view(), name='new_article'),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('articles/<int:id>/edit/', views.ArticleFormUpdateView.as_view(), name='update_article'),
    path('articles/<int:id>/delete/', views.ArticleFormDestroyView.as_view(), name='destroy_article'),
    path('tags/<int:pk>/', views.TagArticleListView.as_view(), name='articles_by_tag'),
    path('tags/', views.TagListView.as_view(), name='tags'),

    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
]
