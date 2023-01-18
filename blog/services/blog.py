from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.http import Http404

from blog import models


def get_articles_sort_new():
    'Returns articles sorted by newest.'
    return models.Article.objects.order_by('-created_at')


def get_articles_sort_top():
    'Returns articles sorted by popularty'
    return models.Article.objects.all()


def get_articles_by_sort(sort):
    if sort == 'new':
        return get_articles_sort_new()
    elif sort == 'top':
        return get_articles_sort_top()
    raise Http404('Page not found')


def get_tags_sort_new():
    'Returns tags sorted by newest'
    return models.Blog.objects.order_by('-created_at')


def get_tags_sort_top():
    'Returns tags sorted by popularty'
    return models.Blog.objects.all()


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
    "Gets or creates a default value language (Others)."
    language, is_created = models.Language.objects.get_or_create(language='Others')
    return language


def get_preffered_language(language):
    """
    Returns a preffered language if one exists, 
    otherwise it calls get_default language.
    """
    try:
        return models.Language.objects.get(language=language)
    except models.Language.DoesNotExist:
        return get_default_language()


def is_author_of_article(author, article_id):
    article = get_article_by_id(article_id)
    return article.author == author


def get_articles_for_search_query(search_query, queryset):
    """
    Returns articles by search query if one exists,
    otherwise it returns a queryset aguments.
    """
    search_query = search_query.get('search_query')
    if search_query:
        return models.Article.objects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(body__icontains=search_query)
        )
    return queryset


def get_blogs_with_counters():
    "Returns a blog list with article and profile counters for each blog."
    return models.Blog.objects.annotate(Count('article', distinct=True), Count('profile', distinct=True)).order_by('name')
