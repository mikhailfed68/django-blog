from django import forms


class SearchForm(forms.Form):
    SORT = [
        ('relevancy', 'Наиболее релевантные'),
        ('new', 'Новые'),
    ]

    TARGET_TYPE = [
        ('articles', 'Статьи'),
        ('tags', 'Теги'),
        ('authors', 'Авторы'),
    ]

    query = forms.CharField(label='Поиск', max_length=255, required=False)
    target_type = forms.ChoiceField(choices=TARGET_TYPE, label='Что искать')
    sort = forms.ChoiceField(choices=SORT, label='Сортировать', required=True, initial='relevancy')
