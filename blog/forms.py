from django import forms

from blog.models import Article, Tag


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'language', 'tags']


class TagFrom(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
