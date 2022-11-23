from django.shortcuts import render, get_object_or_404

from blog.models import Article


def get_latest_created_articles():
    return Article.objects.order_by('-created_at')[:10]


def get_article_by_id(id):
    return get_object_or_404(Article, id=id)