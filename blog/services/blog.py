from django.shortcuts import render, get_object_or_404
from django.http import Http404

from blog import models

def get_articles_sort_new():
    'Return articles sorted by newest.'
    return models.Article.objects.order_by('-created_at')


def get_articles_sort_top():
    'Return articles sorted by popularty'
    return models.Article.objects.all()


def get_articles_by_sort(sort):
    if sort == 'new':
        return get_articles_sort_new()
    elif sort == 'top':
        return get_articles_sort_top()
    raise Http404('Page not found')


def get_tags_sort_new():
    'Return tags sorted by newest'
    return models.Tag.objects.order_by('-created_at')


def get_tags_sort_top():
    'Return tags sorted by popularty'
    return models.Tag.objects.all()


def get_tags_by_sort(sort):
    if sort == 'new':
        return get_tags_sort_new()
    elif sort == 'top':
        return get_tags_sort_top()
    raise Http404('Page not found')


def get_article_by_id(id):
    return get_object_or_404(models.Article, id=id)


def get_articles_by_author(author):
    return models.Article.objects.filter(author=author)


def get_default_language():
    language, is_created = models.Language.objects.get_or_create(language='Others')
    return language.id


def is_author_of_article(user, article_id):
    article = get_article_by_id(article_id)
    return article.author == user
