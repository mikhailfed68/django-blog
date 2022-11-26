from django import forms

from blog.models import Article, Author


class CreateNewArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'author', 'language', 'tags']


class CreateNewAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'surname', 'alias', 'email']
