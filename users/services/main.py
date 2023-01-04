from django.db.models import Count
from django.contrib.auth import get_user_model
from django.http import Http404


def get_user_list():
    return get_user_model().objects.annotate(Count('article'))


def get_users_by_newest():
    return get_user_list().order_by('-date_joined')


def get_users_by_popularty():
    return get_user_list().all()


def get_users_by_articles_count():
    return get_user_list().order_by('-article__count')


def get_users_by_sort(sort):
    if sort == 'new':
        return get_users_by_newest()
    elif sort == 'top':
        return get_users_by_popularty()
    elif sort == 'articles_count':
        return get_users_by_articles_count()
    raise Http404('Page not found')
