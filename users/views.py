from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.conf import settings
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import Group

from users.forms import SignUpForm
from users.services import get_user_list

from blog.services.blog import get_articles_by_author


class SiqnUp(View):
    """
    Регистрирует нового пользователя в блоге и
    выполняет его аутентификацию.
    Для уже авторизованных пользователей выполняет редирект
    на главную страницу.
    """
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        form = SignUpForm()
        return render(
            request,
            'registration/signup.html',
            dict(form=form),
            )

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(Group.objects.get(name='base_members_of_blog'))
            login(request, user)
            messages.success(request, 'Вы успешно зарегестрированы!')
            return redirect(settings.LOGIN_REDIRECT_URL)


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
    queryset = get_user_list()
