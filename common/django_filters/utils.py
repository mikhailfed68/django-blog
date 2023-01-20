from functools import wraps


# Используя django-filter я не нашел стандартного способа
# выполнить сортировку более чем по одному полю и так же
# одновременено использовать поиск в одной форме, так как
# результатом было следующее: "order_by(...).order_by(...)".
# Поэтому был написан декоратор для функции
# (которая передается в параметр 'method' фильтра).
# Декоратор запоминает предыдущие входные параметры функции,
# и передает их с текущими параметрами в эту функцию,
# это позволяет строить в ней желаемое упорядочивание, например:
# "order_by('-profile__count', 'article__count')".
# Так же был написан универсальный фильтр для сортировки объектов
# по возрастанию и убыванию.

ORDER = [('desc', 'По убыванию'), ('asc', 'По возрастанию')]


def memorize(filter_func):
    """
    Memorizes incoming filter parameters and passes
    them to the filter.

    The "memorized" stores the 'name' and 'value' parameters
    of the filter for the past fields that used this filter
    and the current field as well.
    """
    memorized = {}
    @wraps(filter_func)
    def wrapped(self, queryset, name, value):
        memorized[name] = value
        return filter_func(self, queryset, name, value, **memorized)
    return wrapped


@memorize
def order_by_params(self, queryset, name, value, **kwargs):
    """
    Returns a filtered queryset sorted by get parameters
    with a choices (asc or desc).

    The 'asc' - ascending ordering, The 'desc' - descending ordering.

    The result will be ordered with the rest of the fields
    that use this filter using the 'memorize' decorator. For instance:
    "order_by('-profile__count', 'article__count')".
    """
    ordering = []
    for counter, param in kwargs.items():
        if param == 'asc':
            ordering.append(counter)
        elif param == 'desc':
            ordering.append(f'-{counter}')
    return queryset.order_by(*ordering)
