from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('new/', views.CreateNewArticleView.as_view(), name='new_article'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('<int:id>/edit/', views.UpdateArticleView.as_view(), name='update_article'),
    path('<int:id>/delete/', views.DestroyArticleView.as_view(), name='destroy_article'),
    path('tags/', views.TagListView.as_view(), name='tags'),
    path('authors/new/', views.CreateNewAuthorView.as_view(), name='new_author'),
    path('authors/', views.AuthorListView.as_view(), name='authors_list'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author_detail'),
]
