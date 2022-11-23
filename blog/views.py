from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages

from blog import forms
from blog.services.blog_services import get_latest_created_articles, get_article_by_id


def index(request):
    """
    Представление, возвращающее список из последних 10 статей
    на главную страницу сайта.
    """
    if request.path == '/':
        return redirect('blog:index')
    return render(
        request,
        'blog/index.html',
        context={'articles': get_latest_created_articles()})


def article_detail(request, id):
    """
    Представление, возвращающее страницу конкретной статьи.
    """
    article = get_article_by_id(id)
    return render(
        request,
        'blog/article_detail.html',
        context={'article': article})


class CreateNewArticleView(View):
    """
    Возвращает форму создания статьи (метод get)
    или создает новую статью в базе данных
    и выполняет редирект на главную старницу (метод post).
    """
    def get(self, request, *args, **kwargs):
        form = forms.CreateNewArticleForm()
        return render(
            request,
            'blog/new_article.html',
            {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.CreateNewArticleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Новая статья была успешно создана')
            return redirect('blog:index')
        return render(request, 'blog/new_article.html', {'form': form})


class CreateNewAuthorView(View):
    """
    Возвращает форму создания автора (метод get)
    или создает нового автора в базе данных
    и выполняет редирект на главную старницу (метод post).
    """
    def get(self, request, *args, **kwargs):
        form = forms.CreateNewAuthorForm()
        return render(
            request,
            'blog/new_author.html',
            {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.CreateNewAuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль был успешно создан')
            return redirect('blog:index')
        return render(request, 'blog/new_author.html', {'form': form})


class UpdateArticleView(View):
    """
    Возвращает форму редактирования конкретной статьи
    с заполнеными данными (метод get)
    или обновляет статью в базе данных
    и выполняет редирект на страницу обновленной статьи (метод post).
    """
    def get(self, request, *args, **kwargs):
        article_id = kwargs.get('id')
        article = get_article_by_id(article_id)
        form = forms.CreateNewArticleForm(instance=article)
        context = dict(article_id=article_id, form=form)
        return render(request, 'blog/update_article.html', context)

    def post(self, request, *args, **kwargs):
        article_id = kwargs.get('id')
        article = get_article_by_id(article_id)
        form = forms.CreateNewArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статья успешно обновлена')
            return redirect('blog:article_detail', id=article_id)
        context = dict(article_id=article_id, form=form)
        return render(request, 'blog/update_article.html', context)


class DestroyArticleView(View):
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
