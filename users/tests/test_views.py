from django.conf import settings
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from blog.tests.fixtures import create_test_article, create_test_blog
from users.models import User
from users.tests.fixtures import create_test_user, get_test_user_passwd


class SignUpTests(TestCase):
    """Tests the user registration view."""

    def setUp(self):
        self.user_input = dict(
            username="tester",
            first_name="Tester",
            last_name="Testerov",
            email="testing@test.ru",
            password1="qwe123QWE321",
            password2="qwe123QWE321",
        )
        self.resp = self.client.post(
            "/users/register/", data=self.user_input, follow=True, secure=True
        )
        self.created_user = User.objects.get(username=self.user_input.get("username"))

    def test_registration_of_new_user(self):
        self.assertRedirects(self.resp, expected_url=reverse("blog:index"))
        self.assertEqual(
            (self.created_user.username, self.created_user.email),
            (self.user_input.get("username"), self.user_input.get("email")),
        )

    def test_response_has_succses_message(self):
        self.assertContains(self.resp, "Вы успешно зарегестрированы!")

    def test_new_user_in_base_group(self):
        """Checks adding new user to base goup of site members."""
        base_group = Group.objects.get(name=settings.BASE_GROUP)
        self.assertIn(base_group, self.created_user.groups.all())


class AdddingAndRemovingBlogsViewTests(TestCase):
    """Checks AddBlogToUserView and RemoveBlogFromUserView."""

    def setUp(self):
        self.blog = create_test_blog("1")
        self.user = create_test_user("1")
        self.client.force_login(self.user)
        self.user_input = dict(blog_id=self.blog.id, blog_name=self.blog.name)

    def test_views_use_redirect(self):
        add_blog_resp = self.client.post(
            reverse("users:add_blog_to_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )
        remove_blog_resp = self.client.post(
            reverse("users:remove_blog_from_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )

        self.assertRedirects(
            add_blog_resp,
            expected_url=reverse("blog:articles_by_blog", kwargs={"pk": self.blog.pk}),
        )
        self.assertRedirects(
            remove_blog_resp,
            expected_url=reverse("blog:articles_by_blog", kwargs={"pk": self.blog.pk}),
        )

    def test_views_deny_anonymous(self):
        self.client.logout()
        add_blog_resp = self.client.post(
            reverse("users:add_blog_to_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )
        remove_blog_resp = self.client.post(
            reverse("users:remove_blog_from_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )

        self.assertRedirects(
            add_blog_resp,
            expected_url="{}?next={}".format(
                reverse("login"), reverse("users:add_blog_to_profile")
            ),
        )
        self.assertRedirects(
            remove_blog_resp,
            expected_url="{}?next={}".format(
                reverse("login"), reverse("users:remove_blog_from_profile")
            ),
        )

    def test_responses_have_reqiered_buttons(self):
        add_blog_resp = self.client.post(
            reverse("users:add_blog_to_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )
        remove_blog_resp = self.client.post(
            reverse("users:remove_blog_from_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )
        self.assertContains(add_blog_resp, "Отписаться")
        self.assertContains(remove_blog_resp, "Подписаться")

    def test_responses_have_succses_message(self):
        add_blog_resp = self.client.post(
            reverse("users:add_blog_to_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )
        remove_blog_resp = self.client.post(
            reverse("users:remove_blog_from_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )

        self.assertContains(add_blog_resp, f"Вы подписались на блог {self.blog.name}")
        self.assertContains(
            remove_blog_resp, f"Вы отписались от блога {self.blog.name}"
        )

    def test_views_add_blog_to_user_profile(self):
        self.client.post(
            reverse("users:add_blog_to_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )
        self.assertQuerysetEqual(self.user.profile.blogs.all(), [self.blog])

    def test_views_remove_blog_from_user_profile(self):
        self.client.post(
            reverse("users:add_blog_to_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )
        self.client.post(
            reverse("users:remove_blog_from_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )

        self.assertQuerysetEqual(self.user.profile.blogs.all(), [])


class ProfileDetailViewTests(TestCase):
    """Checks ProfileDetailView."""

    def setUp(self):
        self.user = create_test_user("1")
        self.another_user = create_test_user("2")
        self.articles = [
            create_test_article(str(name), self.user) for name in range(13)
        ]
        self.articles.reverse()
        self.resp = self.client.get(
            reverse("users:profile", kwargs={"username": self.user.username}),
            secure=True,
        )

    def test_response_status_code(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.resp, "users/profile.html")

    def test_response_has_author(self):
        self.assertEqual(self.resp.context["author"], self.user)

    def test_response_have_no_private_buttons_for_anonymous(self):
        self.assertNotContains(self.resp, "Создать статью")
        self.assertNotContains(self.resp, "Редактировать")

    def test_response_have_no_private_buttons_for_non_owner(self):
        self.client.force_login(self.another_user)
        self.assertNotContains(self.resp, "Создать статью")
        self.assertNotContains(self.resp, "Редактировать")

    def test_response_have_private_buttons_for_owner(self):
        self.client.login(username=self.user.username, password=get_test_user_passwd())
        resp = self.client.get(
            reverse("users:profile", kwargs={"username": self.user.username}),
            secure=True,
        )
        self.assertContains(resp, "Создать статью")
        self.assertContains(resp, "Редактировать")

    def test_pagination_is_ten(self):
        self.assertIs(self.resp.context["is_paginated"], True)
        self.assertEqual(len(self.resp.context["object_list"]), 10)

    def test_pagination_lists_all_articles(self):
        """Get second page and confirm it has exactly remaining 3 items."""
        second_page_resp = self.client.get(
            reverse("users:profile", kwargs={"username": self.user.username})
            + "?page=2",
            secure=True,
        )

        self.assertIs(second_page_resp.context["is_paginated"], True)
        self.assertEqual(len(second_page_resp.context["object_list"]), 3)

    def test_response_has_exactly_user_articles(self):
        other_articles = [
            create_test_article(str(name), self.another_user) for name in range(20, 23)
        ]
        other_articles.reverse()
        self.assertNotIn(other_articles, self.resp.context["object_list"])


class AdddingAndRemovingAuthorsViewTests(TestCase):
    """Checks AddAuthorToUserView and RemoveAuthorFromUserView."""

    def setUp(self):
        self.user = create_test_user("1")
        self.author_1 = create_test_user("2")
        self.client.force_login(self.user)
        self.user_input = dict(
            author_id=self.author_1.id, author_username=self.author_1.username
        )

    def test_views_use_redirect(self):
        add_author_resp = self.client.post(
            reverse("users:add_author_to_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )
        remove_author_resp = self.client.post(
            reverse("users:remove_author_from_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )

        self.assertRedirects(
            add_author_resp,
            expected_url=reverse(
                "users:profile", kwargs={"username": self.author_1.username}
            ),
        )
        self.assertRedirects(
            remove_author_resp,
            expected_url=reverse(
                "users:profile", kwargs={"username": self.author_1.username}
            ),
        )

    def test_views_deny_anonymous(self):
        self.client.logout()
        add_author_resp = self.client.post(
            reverse("users:add_author_to_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )
        remove_author_resp = self.client.post(
            reverse("users:remove_author_from_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )

        self.assertRedirects(
            add_author_resp,
            expected_url="{}?next={}".format(
                reverse("login"), reverse("users:add_author_to_profile")
            ),
        )
        self.assertRedirects(
            remove_author_resp,
            expected_url="{}?next={}".format(
                reverse("login"), reverse("users:remove_author_from_profile")
            ),
        )

    def test_responses_have_reqiered_buttons(self):
        add_author_resp = self.client.post(
            reverse("users:add_author_to_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )
        remove_author_resp = self.client.post(
            reverse("users:remove_author_from_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )
        self.assertContains(add_author_resp, "Отписаться")
        self.assertContains(remove_author_resp, "Подписаться")

    def test_responses_have_succses_message(self):
        add_author_resp = self.client.post(
            reverse("users:add_author_to_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )
        remove_author_resp = self.client.post(
            reverse("users:remove_author_from_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )

        self.assertContains(
            add_author_resp, f"Вы подписались на {self.author_1.username}"
        )
        self.assertContains(
            remove_author_resp, f"Вы отписались от {self.author_1.username}"
        )

    def test_view_adds_author_to_user_profile(self):
        self.client.post(
            reverse("users:add_author_to_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )
        self.author_2 = create_test_user("3")
        self.client.post(
            reverse("users:add_author_to_profile"),
            data=dict(
                author_id=self.author_2.id, author_username=self.author_2.username
            ),
            follow=True,
            secure=True,
        )
        self.assertQuerysetEqual(
            self.user.profile.following.all(), [self.author_1, self.author_2]
        )
        self.assertQuerysetEqual(self.author_1.followers.all(), [self.user.profile])

    def test_view_removes_author_from_user_profile(self):
        self.client.post(
            reverse("users:add_author_to_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )
        self.client.post(
            reverse("users:remove_author_from_profile"),
            data=self.user_input,
            follow=True,
            secure=True,
        )
        self.assertQuerysetEqual(self.user.profile.following.all(), [])
        self.assertQuerysetEqual(self.author_1.followers.all(), [])
