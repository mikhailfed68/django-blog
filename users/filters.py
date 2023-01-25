import django_filters


class UserFilter(django_filters.FilterSet):
    ORDER = [('desc', 'По убыванию'), ('asc', 'По возрастанию')]

    username = django_filters.CharFilter(
        label='Никнейм',
        field_name='username',
        lookup_expr='icontains',
    )
    by_article_count = django_filters.ChoiceFilter(
        field_name='article__count',
        label='По публикациям',
        choices=ORDER,
        method='order_by_count',
    )

    def order_by_count(self, queryset, name, value):
        """
        Returns a filtered queryset sorted by get parameter
        with a choices (asc or desc).
        """
        ordering = name if value == 'asc' else f'-{name}'
        return queryset.order_by(ordering)
