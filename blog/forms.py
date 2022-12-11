from django import forms

from blog.models import Tag, Article


class TagFrom(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['author']
