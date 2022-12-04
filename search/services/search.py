from django.db.models import Q, Count
from django.http import Http404
from django.contrib.postgres.search import (
    SearchQuery,
    SearchVector,
    SearchRank,
    TrigramWordSimilarity,
)

from blog import models


def search(model, query, expression, **kwargs):
    trigrams = TrigramWordSimilarity(query, expression)
    vector = SearchVector(expression, weight='A')

    for expr in kwargs.values():
        vector += SearchVector(expr, weight='B')
        trigrams += TrigramWordSimilarity(query, expr)

    rank = SearchRank(vector, SearchQuery(query, search_type='websearch'))

    return model.objects.annotate(
        rank=rank,
        similarty=trigrams,
    ).filter(Q(rank__gt=0.3) | Q(similarty__gt=0.3)).order_by('-rank')


def get_articles_for_search_query(search_query):
    return search(
        model=models.Article,
        query=search_query,
        expression='title',
        body='body',
        author_username='author__user__username',
        author_first_name='author__user__first_name',
        author_last_name='author__user__last_name',
    )


def get_authors_for_search_query(search_query):
    authors = search(
        model=models.Author,
        query=search_query,
        expression='user__username',
        fist_name='user__first_name',
        last_name='user__last_name',
        about_yourself='about_yourself',
    )
    return authors.annotate(Count('article'))


def get_tags_for_search_query(search_query):
    return search(
        model=models.Tag,
        query=search_query,
        expression='name',
    )


def get_content_for_search_query(search_query, target_type, sort=None):
    if sort == 'relevancy':
        sorting = '-rank'
    if sort == 'new':
        sorting = '-created_at'

    if target_type =='tags':
        return get_tags_for_search_query(search_query)
    if target_type == 'articles':
        return get_articles_for_search_query(search_query).order_by(sorting)
    if target_type == 'authors':
        sorting = 'user__date_joined' if sort == 'new' else sorting
        return get_authors_for_search_query(search_query).order_by(sorting)
    else:
        raise Http404('Not Found')


def get_template_name(target_type):
    return f'search/{target_type}_search_result.html'