from django.db.models import Count
from django.contrib.auth import get_user_model


def get_users_with_counters():
    "Returns a user list with article counter for each user."
    return get_user_model().objects.annotate(
        Count('article', distinct=True),
    ).order_by('username')


def add_blogs_to_current_user(request, *blogs):
    request.user.profile.blogs.add(*blogs)


def remove_blogs_from_current_user(request, *blogs):
    request.user.profile.blogs.remove(*blogs)
