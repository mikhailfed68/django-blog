from django.db.models import Q
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
    )


def get_authors_for_search_query(search_query):
    return search(
        model=models.Author,
        query=search_query,
        expression='alias',
        first_name='first_name',
        surname='surname',
    )


def get_tags_for_search_query(search_query):
    return search(
        model=models.Tag,
        query=search_query,
        expression='name',
    )


def get_content_for_search_query(search_query, target_type, sort=None):
    if sort == 'new':
        sorting = '-created_at'
    elif sort =='relevancy':
        sorting = '-rank'

    if target_type == 'articles':
        return get_articles_for_search_query(search_query).order_by(sorting)
    if target_type == 'authors':
        return get_authors_for_search_query(search_query).order_by(sorting)
    if target_type =='tags':
        return get_tags_for_search_query(search_query)
    else:
        raise Http404('Not Found')
