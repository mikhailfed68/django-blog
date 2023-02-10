from django.test import TestCase

from users.models import Profile
from users.tests.fixtures import create_test_user


class CreateProfileTests(TestCase):
    """
    Checks creating a new user invokes a 'post_save' signal
    to create a Profile object for the user.
    """

    def test_save_or_create_profile(self):
        user = create_test_user(1)

        try:
            user_proile = Profile.objects.get(user__username=user.username)
        except Profile.DoesNotExist:
            assert False
        else:
            self.assertEqual(user.profile, user_proile)
