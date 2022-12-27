from django import forms

from blog.models import Blog


class TagFrom(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['name']
