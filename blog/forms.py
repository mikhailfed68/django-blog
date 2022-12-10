from django import forms

from blog.models import Tag


class TagFrom(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
