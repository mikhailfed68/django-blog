from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import (
    UserPassesTestMixin,
    PermissionRequiredMixin,
)
from django.views.generic.edit import CreateView

from blog import models, forms
from blog.services.blog import get_article_by_id, is_author_of_article


class IndexListView(generic.ListView):
    """
    Представление, возвращающее список по 10 статей 
    и далее использует пагинацию.
    """
    model = models.Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    paginate_by = 6


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


class ArticleFormCreateView(PermissionRequiredMixin, CreateView):
    """
    Возвращает форму создания статьи (метод get)
    или создает новую статью в базе данных
    и выполняет редирект на главную старницу (метод post).
    """
    permission_required = 'blog.add_article'

    model = models.Article
    fields = ['title', 'body', 'language', 'tags']
    template_name = 'blog/new_article.html'

    def form_valid(self, form):
            new_article = form.save(commit=False)
            new_article.author = self.request.user
            new_article.save()
            form.save_m2m()
            messages.add_message(self.request, messages.SUCCESS, 'Новая статья была успешно создана')
            return redirect('blog:index')


class ArticleFormUpdateView(UserPassesTestMixin, PermissionRequiredMixin, View):
    """
    Возвращает форму редактирования конкретной статьи
    с заполнеными данными (метод get)
    или обновляет статью в базе данных
    и выполняет редирект на страницу обновленной статьи (метод post).
    """
    permission_required = 'blog.change_article'

    def test_func(self):
        return is_author_of_article(user=self.request.user, article_id=self.kwargs.get('id'))

    def get(self, request, *args, **kwargs):
        article_id = self.kwargs.get('id')
        article = get_article_by_id(article_id)
        form = forms.ArticleForm(instance=article)
        context = dict(article_id=article_id, form=form)
        return render(
            request,
            'blog/update_article.html',
            context,
        )

    def post(self, request, *args, **kwargs):
        article_id = self.kwargs.get('id')
        article = get_article_by_id(article_id)
        form = forms.ArticleForm(request.POST, instance=article)
        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.success(request, 'Статья успешно обновлена')
            else:
                messages.info(request, 'Вы не изменили никаких данных.')
            return redirect('blog:article_detail', pk=article_id)
        return render(request,
        'blog/update_article.html',
        dict(article_id=article_id, form=form),
        )


class ArticleFormDestroyView(UserPassesTestMixin, PermissionRequiredMixin, View):
    """
    Удаляет конкретную статью из базы данных
    и выполняет редирект на главную страницу.
    """
    permission_required = 'blog.delete_article'

    def test_func(self):
        return is_author_of_article(user=self.request.user, article_id=self.kwargs.get('id'))

    def post(self, request, *args, **kwargs):
        article = get_article_by_id(self.kwargs.get('id'))
        if article:
            article.delete()
            messages.add_message(request, messages.SUCCESS, 'Статья успешно удалена')
        return redirect('blog:index')
