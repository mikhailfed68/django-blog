import django_filters

# For more information, go to common.django_filters.utils module.
from common.django_filters.utils import ORDER, order_by_params


class BlogFilter(django_filters.FilterSet):
    "Blog filter for searching and ordering by subscribers or articles."
    name = django_filters.CharFilter(
        label='Название блога',
        field_name='name',
        lookup_expr='icontains',
    )
    by_subscriber_count = django_filters.ChoiceFilter(
        field_name='profile__count',
        label='По подписчикам',
        choices=ORDER,
        method='order_by_count',
    )
    by_article_count = django_filters.ChoiceFilter(
        field_name='article__count',
        label='По публикациям',
        choices=ORDER,
        method='order_by_count',
    )

    def order_by_count(self, queryset, name, value, **kwargs):
        "Uses a universal filter function to order blogs"
        return order_by_params(self, queryset, name, value, **kwargs)
