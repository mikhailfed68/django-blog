from django.db.models import Q
from django.contrib.postgres.search import (
    SearchQuery,
    SearchVector,
    SearchRank,
    TrigramWordSimilarity,
)


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
