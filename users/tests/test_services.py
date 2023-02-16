from django.conf import settings
from django.contrib.auth.models import Group
from django.test import TestCase

from blog.tests.fixtures import create_test_article, create_test_blog
from users import services
from users.tests.fixtures import create_test_user


class AddingBaseGoupTests(TestCase):
    """
    Checks the function to add user to base group of site members
    and creates a group if one does not exists.
    """

    def setUp(self):
        self.user_1 = create_test_user(1)
        self.user_2 = create_test_user(2)
        services.add_user_to_base_group_or_create_one(self.user_1)
        self.base_group = Group.objects.get(name=settings.BASE_GROUP)

    def test_add_user_to_base_group_or_create_one(self):
        self.assertIn(self.base_group, self.user_1.groups.all())
        self.assertNotIn(self.base_group, self.user_2.groups.all())


class RetrievingUsers(TestCase):
    """Checks the function of retrieving a specific users list."""

    def test_get_users_with_counters(self):
        """Checks if the 'article__count' field exists for user objects"""
        user_1 = create_test_user(1)
        user_2 = create_test_user(2)
        create_test_article(1, user_1)
        user_qs = services.get_users_with_counters()

        self.assertQuerysetEqual(user_qs, [user_1, user_2])
        self.assertTrue(hasattr(user_qs[0], "article__count"))
        self.assertEqual(user_qs[0].article__count, 1)


class AddingAndRemovingBlogsTests(TestCase):
    """Checks the addition and deletion of blogs to the user."""

    def setUp(self):
        self.user = create_test_user(1)
        self.blog_1 = create_test_blog(1)
        self.blog_2 = create_test_blog(2)
        self.blog_3 = create_test_blog(3)

    def test_add_blogs_to_user(self):
        services.add_blogs_to_user(self.user, self.blog_2, self.blog_3)

        self.assertQuerysetEqual(
            self.user.profile.blogs.all().order_by('created_at'),
            [self.blog_2, self.blog_3],
        )

    def test_remove_blogs_from_user(self):
        services.add_blogs_to_user(self.user, self.blog_1, self.blog_2, self.blog_3)
        services.remove_blogs_from_user(self.user, self.blog_2, self.blog_3)

        self.assertQuerysetEqual(self.user.profile.blogs.all(), [self.blog_1])


class AddingAndRemovingAuthorTests(TestCase):
    """Checks the addition and deletion of authors to the user."""

    def setUp(self):
        self.user = create_test_user(1)
        self.author_1 = create_test_user(2)
        self.author_2 = create_test_user(3)

    def test_add_authors_to_user(self):
        services.add_authors_to_user(self.user, self.author_1, self.author_2)

        self.assertQuerysetEqual(
            self.user.profile.following.all().order_by('date_joined'),
            [self.author_1, self.author_2],
        )

    def test_remove_authors_from_user(self):
        services.add_authors_to_user(self.user, self.author_1, self.author_2)
        services.remove_authors_from_user(self.user, self.author_1)

        self.assertQuerysetEqual(self.user.profile.following.all(), [self.author_2])
