from django.db.models import Count
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission


def add_user_to_base_group_or_create_one(user):
    """
    Add user to base group of users on site
    or creates such group with needed permissons.
    """
    group, created = Group.objects.get_or_create(name=settings.BASE_GROUP)
    if created:
        permissions = Permission.objects.filter(codename__in=settings.PERMISSIONS_FOR_BASE_GROUP)
        group.permissions.set(permissions)
    user.groups.add(group)


def get_users_with_counters():
    "Returns a user list with article counter for each user."
    return get_user_model().objects.annotate(
        Count('article', distinct=True),
    ).order_by('username')


def add_blogs_to_current_user(request, *objs):
    request.user.profile.blogs.add(*objs)


def remove_blogs_from_current_user(request, *objs):
    request.user.profile.blogs.remove(*objs)
