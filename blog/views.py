from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import BaseDeleteView, CreateView, UpdateView

from blog import filters, models
from blog.forms import ArticleForm
from blog.services import (
    get_articles_for_cards,
    get_articles_for_search_query,
    get_blogs_with_counters,
    get_preffered_language,
    get_user_personal_news_feed,
    is_author_of_article,
)
from django.utils.decorators import method_decorator
from django.views.decorators.http import condition


def latest_article(request):
   return models.Article.objects.latest("-created_at").created_at


@method_decorator(condition(last_modified_func=latest_article), name='dispatch')
class IndexListView(ListView):
    """Returns the list of articles to the main page"""

    model = models.Article
    template_name = "blog/index.html"
    context_object_name = "articles"
    paginate_by = 6

    def get_queryset(self):
        search_query = self.request.GET.get("search_query")
        if search_query:
            return get_articles_for_search_query(search_query)
        return get_articles_for_cards()


class PersonalNewsFeedView(LoginRequiredMixin, ListView):
    """Returns personal news feed for current logged-in user."""

    model = models.Article
    template_name = "blog/user_news_feed.html"
    paginate_by = 6

    def get_queryset(self):
        return get_user_personal_news_feed(self.request.user)


class ArticleDetailView(DetailView):
    """Returns the details of article."""

    model = models.Article


class ArticleCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Returns a form for creation an article by GET request
    or creates an new article by POST request.
    """

    permission_required = "blog.add_article"

    model = models.Article
    form_class = ArticleForm
    initial = {"language": get_preffered_language("Русский")}
    template_name = "blog/new_article.html"

    success_message = "Статья успешно создана!"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(
    UserPassesTestMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    """
    Returns a form for updating an article by GET request
    or updates an article by POST request.
    """

    permission_required = "blog.change_article"

    model = models.Article
    form_class = ArticleForm
    template_name = "blog/update_article.html"

    success_message = "Статья успешно обновлена"

    def test_func(self):
        return is_author_of_article(
            author=self.request.user, article_id=self.kwargs.get("pk")
        )


class ArticleDestroyView(
    UserPassesTestMixin, PermissionRequiredMixin, SuccessMessageMixin, BaseDeleteView
):
    """Deletes the article from database."""

    permission_required = "blog.delete_article"

    model = models.Article
    success_url = reverse_lazy("blog:index")

    success_message = "Статья успешно удалена"

    def test_func(self):
        return is_author_of_article(
            author=self.request.user, article_id=self.kwargs.get("pk")
        )


class BlogCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """Creates a new blog."""

    model = models.Blog
    fields = ["name", "description"]
    template_name_suffix = "_create_form"
    success_message = "Новый блог успешно создан."


class BlogListView(ListView):
    """Returns the list of blogs."""

    model = models.Blog
    paginate_by = 5

    def get_queryset(self):
        self.filter = filters.BlogFilter(
            self.request.GET,
            queryset=get_blogs_with_counters(),
            request=self.request,
        )
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filter
        return context


class BlogDetailView(SingleObjectMixin, ListView):
    """Retruns the details of blog and the list of articles its blog."""

    template_name = "blog/articles_by_blog.html"
    context_object_name = "blog"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=models.Blog.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.article_set.all()
