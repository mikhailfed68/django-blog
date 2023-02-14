import datetime

from django.core.cache import cache
from django.test import TestCase
from django.utils import timezone

from blog.tests.fixtures import create_test_article
from users.tests.fixtures import create_test_user


class ArticleModelTest(TestCase):
    def setUp(self):
        self.user = create_test_user("1")
        self.article = create_test_article("1", self.user)

    def tearDown(self):
        cache.clear()

    def test_was_updated_recently_with_new_article(self):
        """
        was_updated_recently() returns True for articles
        whose updated_at is within the last day.
        """
        self.assertIs(self.article.was_updated_recently(), True)

    def test_was_updated_recently(self):
        """
        was_updated_recently() returns Flase for articles
        whose updated_at is older than 1 day.
        """
        time_created = timezone.now() - datetime.timedelta(days=5)
        time_updated = timezone.now() - datetime.timedelta(days=4)
        self.article.created_at = time_created
        self.article.updated_at = time_updated
        self.assertIs(self.article.was_updated_recently(), False)
