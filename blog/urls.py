from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),

    path('new/', views.ArticleFormCreateView.as_view(), name='new_article'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('<int:id>/edit/', views.ArticleFormUpdateView.as_view(), name='update_article'),
    path('<int:id>/delete/', views.ArticleFormDestroyView.as_view(), name='destroy_article'),
    path('tags/<int:pk>/', views.TagArticleListView.as_view(), name='articles_by_tag'),

    path('tags/', views.TagListView.as_view(), name='tags'),

    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('authors/new/', views.AuthorFormCreateView.as_view(), name='new_author'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
]
