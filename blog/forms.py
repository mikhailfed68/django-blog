from django import forms

from blog.models import Article, Author, Tag


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'author', 'language', 'tags']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'surname', 'alias', 'email']


class TagFrom(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


class SearchForm(forms.Form):
    SORTING = [
        ('relevancy', 'Наиболее релевантные'),
        ('new', 'Новые'),
    ]
    query = forms.CharField(label='Поиск', max_length=255, required=False)
    sort = forms.ChoiceField(choices=SORTING, label='Сортировать', required=True, initial='relevancy')
