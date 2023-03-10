import django_filters

from blog.models import Article


class ArticleFilter(django_filters.FilterSet):
    article_name = django_filters.CharFilter(
        label="Название публикации",
        field_name="title",
        lookup_expr="icontains",
    )
    range = django_filters.DateRangeFilter(
        field_name="created_at", label="Период публикации"
    )

    class Meta:
        model = Article
        fields = ["article_name", "range"]


class BlogFilter(django_filters.FilterSet):
    """Blog filter for searching and ordering by subscribers or articles."""

    ORDER = [("desc", "По убыванию"), ("asc", "По возрастанию")]

    name = django_filters.CharFilter(
        label="Название блога",
        field_name="name",
        lookup_expr="icontains",
    )
    by_followers_count = django_filters.ChoiceFilter(
        field_name="user__count",
        label="По подписчикам",
        choices=ORDER,
        method="order_by_count",
    )
    by_article_count = django_filters.ChoiceFilter(
        field_name="article__count",
        label="По публикациям",
        choices=ORDER,
        method="order_by_count",
    )

    def order_by_count(self, queryset, name, value):
        """
        Returns a filtered queryset sorted by get parameters
        with a choices (asc or desc).
        """
        ordering_param = {
            counter: param
            for (counter, param) in self.request.GET.items()
            if counter in ("by_article_count", "by_followers_count")
        }

        ordering = []
        for counter, param in ordering_param.items():
            field_of_param = (
                "user__count" if counter == "by_followers_count" else "article__count"
            )
            if param == "asc":
                ordering.append(field_of_param)
            elif param == "desc":
                ordering.append(f"-{field_of_param}")
        return queryset.order_by(*ordering)


class BookmarkFilter(django_filters.FilterSet):
    article_name = django_filters.CharFilter(
        label="Название публикации",
        field_name="title",
        lookup_expr="icontains",
    )
    range = django_filters.DateRangeFilter(
        field_name="bookmarksrelation__date_added", label="Период добавления"
    )

    class Meta:
        model = Article
        fields = ["article_name", "range"]
