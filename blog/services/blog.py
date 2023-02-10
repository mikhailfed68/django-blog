from django.db.models import Count, Q
from django.shortcuts import get_object_or_404

from blog import models


def get_default_language():
    """Gets or creates a default value language (Others)."""
    language, is_created = models.Language.objects.get_or_create(language="Others")
    return language


def get_preffered_language(language):
    """
    Returns a preffered language if one exists,
    otherwise it calls get_default_language.
    """
    try:
        return models.Language.objects.get(language=language)
    except models.Language.DoesNotExist:
        return get_default_language()


def is_author_of_article(author, article_id):
    article = get_object_or_404(models.Article, id=article_id)
    return article.author == author


def get_articles_for_search_query(search_query, queryset):
    """
    Returns articles by search query if one exists,
    otherwise it returns a queryset arguments.
    """
    search_query = search_query.get("search_query")
    if search_query:
        return models.Article.objects.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(body__icontains=search_query)
        )
    return queryset


def get_blogs_with_counters():
    """Returns a blog list with article and profile counters for each blog."""
    return models.Blog.objects.annotate(
        Count("article", distinct=True), Count("profile", distinct=True)
    ).order_by("name")


def get_user_personal_news_feed(user):
    """Retruns the user personal news feed by his blogs."""
    user_blogs = user.profile.blogs.all()
    user_feed_articles = models.Article.objects.filter(blogs__in=user_blogs).distinct()
    return user_feed_articles
