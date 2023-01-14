import django_filters
from users.models import User


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains', label='Username')

    class Meta:
        model = User
        fields = ['username']
