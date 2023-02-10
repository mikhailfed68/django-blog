import django_filters


class UserFilter(django_filters.FilterSet):
    ORDER = [("desc", "По убыванию"), ("asc", "По возрастанию")]

    username = django_filters.CharFilter(
        label="Никнейм",
        field_name="username",
        lookup_expr="icontains",
    )
    by_article_count = django_filters.ChoiceFilter(
        field_name="article__count",
        label="По публикациям",
        choices=ORDER,
        method="order_by_count",
    )
    by_followers_count = django_filters.ChoiceFilter(
        field_name="followers__count",
        label="По подписчикам",
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
                "followers__count"
                if counter == "by_subscriber_count"
                else "article__count"
            )
            if param == "asc":
                ordering.append(field_of_param)
            elif param == "desc":
                ordering.append(f"-{field_of_param}")
        return queryset.order_by(*ordering)
