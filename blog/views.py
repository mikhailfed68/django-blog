from django.views import generic
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count

from blog.services.blog_services import get_latest_created_articles, get_article_by_id
from blog import models
from blog import forms


class IndexListView(generic.ListView):
    """
    Представление, возвращающее список по 10 статей 
    и далее использует пагинацию.
    """
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    queryset = get_latest_created_articles()
    paginate_by = 10


class ArticleDetailView(generic.DetailView):
    """Возвращает данные конкретной статьи."""
    model = models.Article


class TagListView(generic.ListView):
    """
    Возвращает список по 20 последних тегов
    и далее использует пагинацию.
    """
    model = models.Tag
    template_name = 'blog/tags/tag_list.html'
    context_object_name = 'tags'
    paginate_by = 20


class TagArticleListView(generic.ListView):
    """
    Возвращает список по 10 последних статей
    по конкретному тегу и далее использует пагинацию
    """
    template_name = 'blog/articles_by_tag.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        self.tag = get_object_or_404(models.Tag, pk=self.kwargs['pk'])
        return models.Article.objects.filter(tags=self.tag).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class AuthorListView(generic.ListView):
    """
    Возвращает список авторов в блоге,
    количество статей для каждого автора и реализует
    пагинацию по 6 статей.
    """
    template_name = 'blog/authors/author_list.html'
    context_object_name = 'authors'
    paginate_by = 6

    def get_queryset(self):
        return models.Author.objects.annotate(Count('article')).order_by('-article__count')


class AuthorDetailView(generic.ListView):
    """
    Возвращает страницу конкретного автора
    и все опубликованные статьи автора с пагинацией по 10 статей.
    """
    template_name = 'blog/authors/author_detail.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        self.author = get_object_or_404(models.Author, pk=self.kwargs['pk'])
        return models.Article.objects.filter(author=self.author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context


class AuthorFormCreateView(View):
    """
    Возвращает форму создания автора (метод get)
    или создает нового автора в базе данных
    и выполняет редирект на главную старницу (метод post).
    """
    def get(self, request, *args, **kwargs):
        form = forms.AuthorForm()
        return render(
            request,
            'blog/authors/new_author.html',
            {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль был успешно создан')
            return redirect('blog:authors')
        return render(request, 'blog/authors/new_author.html', {'form': form})


class ArticleFormCreateView(View):
    """
    Возвращает форму создания статьи (метод get)
    или создает новую статью в базе данных
    и выполняет редирект на главную старницу (метод post).
    """
    def get(self, request, *args, **kwargs):
        form = forms.ArticleForm()
        return render(
            request,
            'blog/new_article.html',
            {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Новая статья была успешно создана')
            return redirect('blog:index')
        return render(request, 'blog/new_article.html', {'form': form})


class ArticleFormUpdateView(View):
    """
    Возвращает форму редактирования конкретной статьи
    с заполнеными данными (метод get)
    или обновляет статью в базе данных
    и выполняет редирект на страницу обновленной статьи (метод post).
    """
    def get(self, request, *args, **kwargs):
        article_id = kwargs.get('id')
        article = get_article_by_id(article_id)
        form = forms.ArticleForm(instance=article)
        context = dict(article_id=article_id, form=form)
        return render(request, 'blog/update_article.html', context)

    def post(self, request, *args, **kwargs):
        article_id = kwargs.get('id')
        article = get_article_by_id(article_id)
        form = forms.ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статья успешно обновлена')
            return redirect('blog:article_detail', pk=article_id)
        context = dict(article_id=article_id, form=form)
        return render(request, 'blog/update_article.html', context)


class ArticleFormDestroyView(View):
    """
    Удаляет конкретную статью из базы данных
    и выполняет редирект на главную страницу.
    """
    def post(self, request, *args, **kwargs):
        article_id = kwargs.get('id')
        article = get_article_by_id(article_id)
        if article:
            article.delete()
            messages.add_message(request, messages.SUCCESS, 'Статья успешно удалена')
        return redirect('blog:index')
