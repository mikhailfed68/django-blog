from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, BaseDeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin

from blog import models
from blog.services.blog import (
    is_author_of_article,
    get_articles_by_sort,
    get_tags_by_sort,
)


class IndexListView(ListView):
    "Returns the list of articles to the main page"
    model = models.Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self):
        "If sort parameter exists, it'll retruns a sorted queryset."
        sort = self.request.GET.get('sort')
        if sort:
            return get_articles_by_sort(sort)
        return super().get_queryset()


class ArticleDetailView(DetailView):
    "Returns the details of article."
    model = models.Article


class BlogListView(ListView):
    "Returns the list of blogs."
    model = models.Blog
    context_object_name = 'blogs'
    paginate_by = 20

    def get_queryset(self):
        "If sort parameter exists, it'll retrun a sorted queryset."
        sort = self.request.GET.get('sort')
        if sort:
            return get_tags_by_sort(sort)
        return super().get_queryset()


class BlogDetailView(SingleObjectMixin, ListView):
    "Retruns the details of blog and the list of articles its blog." 
    template_name = 'blog/articles_by_blog.html'
    context_object_name = 'blog'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=models.Blog.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.article_set.all()


class ArticleCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Returns a form for creation an article by GET request
    or creates an new article by POST request.    
    """
    permission_required = 'blog.add_article'

    model = models.Article
    fields = ['title', 'body', 'language', 'blogs']
    template_name = 'blog/new_article.html'

    success_message = 'Статья успешно создана!'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(
        UserPassesTestMixin, PermissionRequiredMixin,
        SuccessMessageMixin, UpdateView):
    """
    Returns a form for updating an article by GET request
    or updates an article by POST request.
    """
    permission_required = 'blog.change_article'

    model = models.Article
    fields = ['title', 'body', 'language', 'blogs']
    template_name = 'blog/update_article.html'

    success_message = 'Статья успешно обновлена'

    def test_func(self):
        return is_author_of_article(author=self.request.user, article_id=self.kwargs.get('pk'))


class ArticleDestroyView(
        UserPassesTestMixin, PermissionRequiredMixin,
        SuccessMessageMixin, BaseDeleteView):
    "Deletes the article from database."
    permission_required = 'blog.delete_article'

    model = models.Article
    success_url = reverse_lazy('blog:index')

    success_message = 'Статья успешно удалена'

    def test_func(self):
        return is_author_of_article(author=self.request.user, article_id=self.kwargs.get('pk'))
