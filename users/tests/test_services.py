from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import Group

from users.services import main
from users.tests.fixtures import create_test_user
from blog.tests.fixtures import create_test_blog, create_test_article


class AddingBaseGoupTests(TestCase):
    """
    Checks the function to add user to base group of site members
    and creates a group if one does not exists.
    """
    def setUp(self):
        self.user_1 = create_test_user(1)
        self.user_2 = create_test_user(2)
        main.add_user_to_base_group_or_create_one(self.user_1)
        self.base_group = Group.objects.get(name=settings.BASE_GROUP)

    def test_add_user_to_base_group_or_create_one(self):
        self.assertIn(self.base_group, self.user_1.groups.all())
        self.assertNotIn(self.base_group, self.user_2.groups.all())


class RetrievingUsers(TestCase):
    "Checks the function of retrieving a specific users list."
    def test_get_users_with_counters(self):
        "Checks if the 'article__count' field exists for user objects"
        user_1 = create_test_user(1)
        user_2 = create_test_user(2)
        create_test_article(1, user_1)
        user_qs = main.get_users_with_counters()

        self.assertQuerysetEqual(user_qs, [user_1, user_2])
        self.assertTrue(hasattr(user_qs[0], 'article__count'))
        self.assertEqual(user_qs[0].article__count, 1)


class AddingAndRemovingBlogsTests(TestCase):
    "Checks the addition and deletion of blogs to the user."
    def setUp(self):
        class FakeRequest:
            "Instantiates a stub for request."
            user = create_test_user(1)

        self.request = FakeRequest()
        self.blog_1 = create_test_blog(1)
        self.blog_2 = create_test_blog(2)
        self.blog_3 = create_test_blog(3)

    def test_add_blogs_to_current_user(self):
        main.add_blogs_to_current_user(self.request, self.blog_1.pk)
        main.add_blogs_to_current_user(self.request, self.blog_2, self.blog_3)

        self.assertQuerysetEqual(
            self.request.user.profile.blogs.all(),
            [self.blog_1, self.blog_2, self.blog_3]
        )

    def test_remove_blogs_from_current_user(self):
        main.add_blogs_to_current_user(self.request, self.blog_1, self.blog_2, self.blog_3)
        main.remove_blogs_from_current_user(self.request, self.blog_2, self.blog_3)

        self.assertQuerysetEqual(self.request.user.profile.blogs.all(), [self.blog_1])
