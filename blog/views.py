from django.shortcuts import render

from blog.services.blog_services import get_latest_created_articles


def index(request):
    """
    Представление, возвращающее список из последних 10 статей
    на главную страницу сайта.
    """
    return render(
        request,
        'blog/index.html',
        context={'articles': get_latest_created_articles()})
