from django.shortcuts import render, get_object_or_404

from blog import models


def get_latest_created_articles():
    return models.Article.objects.order_by('-created_at')[:10]


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
