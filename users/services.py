from django.db.models import Count
from django.contrib.auth import get_user_model


def get_user_list():
    return get_user_model().objects.annotate(Count('article')).order_by('-article__count')
