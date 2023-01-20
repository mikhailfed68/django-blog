import django_filters

# For more information, go to common.django_filters.utils module.
from common.django_filters.utils import ORDER,  order_by_params


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        label='Username',
        field_name='username',
        lookup_expr='icontains',
    )
    by_article_count = django_filters.ChoiceFilter(
        field_name='article__count',
        label='По публикациям',
        choices=ORDER,
        method='order_by_count',
    )

    def order_by_count(self, queryset, name, value, **kwargs):
        "Uses a universal filter function to order users"
        return order_by_params(self, queryset, name, value, **kwargs)
