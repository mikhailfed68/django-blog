from django import forms

from blog.models import Article, Author, Tag


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'author', 'language', 'tags']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'surname', 'alias', 'email', 'tags']


class TagFrom(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
