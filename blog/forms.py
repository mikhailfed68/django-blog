from django import forms

from blog.models import Blog, Article


class TagFrom(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['name']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['author']
