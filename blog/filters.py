import django_filters
from blog.models import Blog


class BlogFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Название блога')

    class Meta:
        model = Blog
        fields = ['name']
