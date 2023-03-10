from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db.models import Count


def add_user_to_base_group_or_create_one(user):
    """
    Add user to base group of users on the site
    or creates such group with the necessary
    permissions if one does not exist.
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
    Returns a user list with article counter
    and follower counter for each user.
    """
    return (
        get_user_model()
        .objects.annotate(
            Count("article", distinct=True),
            Count("followers", distinct=True),
        )
        .order_by("-date_joined")
        .only(
            "username",
            "first_name",
            "last_name",
            "profile_picture",
            "about_me",
            "following",
        )
    )


def get_users_with_all_counter():
    """
    Returns 'get_users_with_counters' and also
    user counter that the user is following.
    """
    return get_users_with_counters().annotate(
        following__count=Count("following", distinct=True),
    )


def get_user_following_list(user):
    """
    Returns a list of users that the user is following.
    Users in the list has its own article counter
    and follower counter.
    """
    return (
        user.following.annotate(
            Count("article", distinct=True),
            Count("followers", distinct=True),
        )
        .order_by("-date_joined")
        .only("username", "first_name", "last_name", "profile_picture", "about_me")
    )


def add_blogs_to_user(user, *blogs):
    """Add blogs to the list that the user is following."""
    user.blogs.add(*blogs)


def remove_blogs_from_user(user, *blogs):
    """Remove blogs from the list that the user is following."""
    user.blogs.remove(*blogs)


def add_authors_to_user(user, *authors):
    """Add authors to the list that the user is following."""
    user.following.add(*authors)


def remove_authors_from_user(user, *authors):
    """Remove authors from the list that the user is following."""
    user.following.remove(*authors)
