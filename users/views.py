from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.transaction import atomic
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import BaseDeleteView

from users import models
from users.filters import UserFilter
from users.forms import ChangeProfileForm, CustomUserChangeForm, SignUpForm
from users.services import (
    add_authors_to_user,
    add_blogs_to_user,
    add_user_to_base_group_or_create_one,
    get_user_following_list,
    get_users_with_all_counter,
    get_users_with_counters,
    remove_authors_from_user,
    remove_blogs_from_user,
)


@method_decorator(decorator=atomic, name="dispatch")
class SiqnUp(CreateView):
    """Registers the user on the site."""

    model = models.User
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        user = form.save()
        add_user_to_base_group_or_create_one(user)
        login(self.request, user)
        messages.success(self.request, "Вы успешно зарегестрированы!")
        return redirect(self.success_url)


class ProfileDetailView(SingleObjectMixin, ListView):
    """
    Return the user profile by the 'username' slug
    and its published articles list.
    """

    template_name = "users/profile.html"
    context_object_name = "author"
    slug_field = "username"
    slug_url_kwarg = "username"
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        """
        Assigning the desired User object to
        object atrribute for further processing.
        """
        self.object = self.get_object(
            queryset=get_users_with_all_counter(),
        )
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.article_set.all().defer("language_id", "body")


class UserListView(ListView):
    """Rerturn the registred users list."""

    model = models.User
    paginate_by = 5

    def get_queryset(self):
        self.filter = UserFilter(
            self.request.GET,
            queryset=get_users_with_counters(),
            request=self.request,
        )
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filter
        return context


class UserFollowingListView(LoginRequiredMixin, ListView):
    """Returns a followng list of current user."""

    model = models.User
    paginate_by = 5

    def get_queryset(self):
        self.filter = UserFilter(
            self.request.GET,
            queryset=get_user_following_list(self.request.user),
            request=self.request,
        )
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filter
        return context


@method_decorator(decorator=atomic, name="dispatch")
class UserUpdateView(UserPassesTestMixin, PermissionRequiredMixin, View):
    """Update User data as well as his Profile data."""

    permission_required = "users.change_profile"

    def test_func(self):
        "Verify user identity by session user object"
        return self.request.user.get_username() == self.kwargs.get("username")

    def get(self, request, *args, **kwargs):
        user_form = CustomUserChangeForm(instance=request.user)
        profile_form = ChangeProfileForm(instance=request.user.profile)
        return render(
            request,
            "users/update_user.html",
            dict(user_form=user_form, profile_form=profile_form),
        )

    def post(self, request, *args, **kwargs):
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ChangeProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile_form.save()
            messages.success(request, "Вы успешно обновили свои данные")
            return redirect("users:update_user", username=user.get_username())
        return render(
            request,
            "users/update_user.html",
            dict(user_form=user_form, profile_form=profile_form),
        )


@method_decorator(decorator=atomic, name="dispatch")
class UserDestroyView(
    UserPassesTestMixin, PermissionRequiredMixin, SuccessMessageMixin, BaseDeleteView
):
    """Delete user."""

    permission_required = "users.delete_profile"

    model = get_user_model()
    slug_field = "username"
    slug_url_kwarg = "username"
    success_url = settings.LOGOUT_REDIRECT_URL

    success_message = "Аккаунт успешно удален"

    def test_func(self):
        "Verify user identity by session user object"
        return self.request.user.get_username() == self.kwargs.get("username")


@method_decorator(decorator=atomic, name="dispatch")
class AddBlogToProfileView(LoginRequiredMixin, SuccessMessageMixin, View):
    """
    Add blog to the list that the current authenticated user is following.
    """

    def post(self, request, *args, **kwargs):
        blog_id = request.POST.get("blog_id")
        blog_name = request.POST.get("blog_name")
        add_blogs_to_user(request.user, blog_id)
        messages.success(request, f"Вы подписались на блог {blog_name}")
        return redirect("blog:articles_by_blog", pk=blog_id)


@method_decorator(decorator=atomic, name="dispatch")
class RemoveBlogFromProfileView(LoginRequiredMixin, View):
    """
    Remove blog from the list that the current authenticated user is following.
    """

    def post(self, request, *args, **kwargs):
        blog_id = request.POST.get("blog_id")
        blog_name = request.POST.get("blog_name")
        remove_blogs_from_user(request.user, blog_id)
        messages.success(request, f"Вы отписались от блога {blog_name}")
        return redirect("blog:articles_by_blog", pk=blog_id)


@method_decorator(decorator=atomic, name="dispatch")
class AddAuthorToProfileView(LoginRequiredMixin, View):
    """
    Add author to the list that the current authenticated user is following.
    """

    def post(self, request, *args, **kwargs):
        author_id = request.POST.get("author_id")
        author_username = request.POST.get("author_username")
        add_authors_to_user(request.user, author_id)
        messages.success(request, f"Вы подписались на {author_username}")
        return redirect("users:profile", username=author_username)


@method_decorator(decorator=atomic, name="dispatch")
class RemoveAuthorFromProfileView(LoginRequiredMixin, View):
    """
    Remove author from the list that the current
    authenticated user is following.
    """

    def post(self, request, *args, **kwargs):
        author_id = request.POST.get("author_id")
        author_username = request.POST.get("author_username")
        remove_authors_from_user(request.user, author_id)
        messages.success(request, f"Вы отписались от {author_username}")
        return redirect("users:profile", username=author_username)
