from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.conf import settings
from django.views import View
from django.views.generic import ListView, CreateView
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import logout_then_login

from users.forms import SignUpForm, CustomUserChangeForm, ChangeProfileForm
from users.services import get_user_list, get_users_by_sort
from users import models

from blog.services.blog import get_articles_by_author


class SiqnUp(CreateView):
    model = models.User
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        user = form.save()
        user.groups.add(Group.objects.get(name='base_members_of_blog'))
        login(self.request, user)
        messages.success(self.request, 'Вы успешно зарегестрированы!')
        return redirect(self.success_url)


class ProfileDetailView(ListView):
    """
    Возвращает страницу конкретного автора
    и все опубликованные статьи автора с пагинацией по 10 статей.
    """

    template_name = 'users/profile.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        self.author = get_object_or_404(get_user_model(), username=self.kwargs['username'])
        return get_articles_by_author(author=self.author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context


class UserListView(ListView):
    """
    Возвращает список авторов в блоге и реализует
    пагинацию по 10 статей.
    """
    context_object_name = 'authors'
    paginate_by = 10

    def get_queryset(self):
        "If sort parameter exists, it'll retrun a sorted queryset"
        sort = self.request.GET.get('sort')
        if sort:
            return get_users_by_sort(sort)
        return get_user_list()


class UserUpdateView(UserPassesTestMixin, PermissionRequiredMixin, View):
    "This view update data User as well as his data Profile"
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
        profile_form = ChangeProfileForm(request.POST, instance=request.user.profile)
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


class UserDestroyView(UserPassesTestMixin, PermissionRequiredMixin, View):
    "This view destroy user"
    permission_required = 'users.delete_user'

    def test_func(self):
        return self.request.user.get_username() == self.kwargs.get('username')

    def post(self, request, *args, **kwargs):
        request.user.delete()
        messages.success(request, 'Аккаунт успешно удален')
        return logout_then_login(request)
