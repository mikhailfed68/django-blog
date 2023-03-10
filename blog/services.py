from django.db.models import Count, Q
from django.shortcuts import get_object_or_404

from blog import models


def is_author_of_article(author, article_id):
    article = get_object_or_404(models.Article, id=article_id)
    return article.author == author


def get_blogs_with_counters():
    """
    Returns a blog list with article
    and profile counters for each blog.
    """
    return (
        models.Blog.objects.annotate(
            Count("article", distinct=True),
            Count("user", distinct=True),
        )
        .order_by("created_at")
        .only("name", "description")
    )


def get_articles_for_cards():
    return models.Article.objects.order_by("-created_at").defer(
        "body", "author_id", "language_id"
    )


def get_articles_for_search_query(search_query):
    """Returns articles by search query."""
    return get_articles_for_cards().filter(
        Q(title__icontains=search_query)
        | Q(description__icontains=search_query)
        | Q(body__icontains=search_query)
    )


def get_personal_news_feed(user):
    """
    Retruns the user personal news feed by his blogs
    and authors that the user is following.
    """
    user_blogs = user.blogs.all().values("id")
    user_following_list = user.following.all().values("id")

    return (
        get_articles_for_cards()
        .filter(Q(blogs__in=user_blogs) | Q(author__in=user_following_list))
        .distinct()
    )
