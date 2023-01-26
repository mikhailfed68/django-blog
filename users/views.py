from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
from django.views.generic import ListView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import BaseDeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import (
    PermissionRequiredMixin,
    UserPassesTestMixin,
    LoginRequiredMixin,
)

from users import models
from users.forms import SignUpForm, CustomUserChangeForm, ChangeProfileForm
from users.filters import UserFilter
from users.services.main import (
    add_user_to_base_group_or_create_one,
    get_users_with_counters,
    add_blogs_to_current_user,
    remove_blogs_from_current_user,
)


class SiqnUp(CreateView):
    model = models.User
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        user = form.save()
        add_user_to_base_group_or_create_one(user)
        login(self.request, user)
        messages.success(self.request, 'Вы успешно зарегестрированы!')
        return redirect(self.success_url)


class ProfileDetailView(SingleObjectMixin, ListView):
    """
    Return the user profile by the 'username' slug,
    as well as all of its published articles list.
    """
    template_name = 'users/profile.html'
    context_object_name = 'author'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        "Assigning the desired User object to object atrribute for further processing."
        self.object = self.get_object(queryset=get_user_model().objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.article_set.all()


class UserListView(ListView):
    "Rerturn the registred users list."
    model = models.User
    paginate_by = 3

    def get_queryset(self):
        self.filter = UserFilter(
            self.request.GET,
            queryset=get_users_with_counters(),
            request=self.request,
        )
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


class UserUpdateView(UserPassesTestMixin, PermissionRequiredMixin, View):
    "Update User data as well as his Profile data"
    permission_required = 'users.change_user'

    def test_func(self):
        "Verify user identity by session user object"
        return self.request.user.get_username() == self.kwargs.get('username')

    def get(self, request, *args, **kwargs):
        user_form = CustomUserChangeForm(instance=request.user)
        profile_form = ChangeProfileForm(instance=request.user.profile)
        return render(
            request,
            'users/update_user.html',
            dict(user_form=user_form, profile_form=profile_form),
        )

    def post(self, request, *args, **kwargs):
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ChangeProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile_form.save()
            messages.success(request, 'Вы успешно обновили свои данные')
            return redirect('users:update_user', username=user.get_username())
        return render(
            request,
            'users/update_user.html',
            dict(user_form=user_form, profile_form=profile_form),
        )


class UserDestroyView(
        UserPassesTestMixin, PermissionRequiredMixin,
        SuccessMessageMixin, BaseDeleteView):
    "This view delete user"
    permission_required = 'users.delete_user'

    model = get_user_model()
    slug_field = 'username'
    slug_url_kwarg = 'username'
    success_url = settings.LOGOUT_REDIRECT_URL

    success_message = 'Аккаунт успешно удален'

    def test_func(self):
        "Verify user identity by session user object"
        return self.request.user.get_username() == self.kwargs.get('username')


class AddBlogToUserView(LoginRequiredMixin, SuccessMessageMixin, View):
    "Add blog to profile of current user."

    def post(self, request, *args, **kwargs):
        blog_id = request.POST.get('blog_id')
        blog_name = request.POST.get('blog_name')
        add_blogs_to_current_user(request, blog_id)
        messages.success(request, f'Вы подписались на блог {blog_name}')
        return redirect('blog:articles_by_blog', pk=blog_id)


class RemoveBlogFromUserView(LoginRequiredMixin, View):
    "Remove blog from profile of current user."

    def post(self, request, *args, **kwargs):
        blog_id = request.POST.get('blog_id')
        blog_name = request.POST.get('blog_name')
        remove_blogs_from_current_user(request, blog_id)
        messages.success(request, f'Вы отписались от блога {blog_name}')
        return redirect('blog:articles_by_blog', pk=blog_id)
