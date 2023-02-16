from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db.models import Count


def add_user_to_base_group_or_create_one(user):
    """
    Add user to base group of users on site
    or creates such group with needed permissons.
    """
    group, created = Group.objects.get_or_create(name=settings.BASE_GROUP)
    if created:
        permissions = Permission.objects.filter(
            codename__in=settings.PERMISSIONS_FOR_BASE_GROUP
        )
        group.permissions.set(permissions)
    user.groups.add(group)


def get_users_with_counters():
    """
    Returns a user list with article
    and followers counters for each user.
    """
    return (
        get_user_model()
        .objects.annotate(
            Count("article", distinct=True),
            Count("followers", distinct=True),
        )
        .select_related("profile")
        .order_by("date_joined")
        .only("username", "first_name", "last_name", "profile")
    )


def get_users_for_profile():
    """
    Returns a user list with article
    and followers counters for each user.
    """
    return get_users_with_counters().annotate(
        following__count=Count("profile__following", distinct=True),
    )


def get_user_following_list(user):
    """
    Returns a followng list with article
    and followers counters for each user.
    """
    return (
        user.profile.following.annotate(
            Count("article", distinct=True),
            Count("followers", distinct=True),
        )
        .order_by("date_joined")
        .select_related("profile")
        .only("username", "first_name", "last_name", "profile")
    )


def add_blogs_to_user(user, *blogs):
    """Add blogs to user's blog list."""
    user.profile.blogs.add(*blogs)


def remove_blogs_from_user(user, *blogs):
    """Remove blogs from user's blog list."""
    user.profile.blogs.remove(*blogs)


def add_authors_to_user(user, *authors):
    """Add authors to user's following list."""
    user.profile.following.add(*authors)


def remove_authors_from_user(user, *authors):
    """Remove authors from user's following list."""
    user.profile.following.remove(*authors)
