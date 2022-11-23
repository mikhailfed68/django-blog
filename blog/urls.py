from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.CreateNewArticleView.as_view(), name='new_article'),
    path('<int:id>/', views.article_detail, name='article_detail'),
    path('<int:id>/edit/', views.UpdateArticleView.as_view(), name='update_article'),
    path('<int:id>/delete/', views.DestroyArticleView.as_view(), name='destroy_article'),
    path('authors/new/', views.CreateNewAuthorView.as_view(), name='new_author'),
]