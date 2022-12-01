from django.shortcuts import render, get_object_or_404

from blog import models


def get_latest_created_articles():
    return models.Article.objects.order_by('-created_at')[:10]


def get_article_by_id(id):
    return get_object_or_404(models.Article, id=id)


def get_default_language():
    language, is_created = models.Language.objects.get_or_create(language='Others')
    return language.id
