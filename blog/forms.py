from django import forms
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError

from blog.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'description', 'title_photo', 'body', 'language', 'blogs']
    
    def clean_title_photo(self):
        title_photo = self.cleaned_data.get('title_photo')

        if title_photo:
            width, height = get_image_dimensions(title_photo)
            if (width < 771) or (height < 482):
                raise ValidationError(
                    "Слишком маленькое изображение, минимальная высота и ширина - 771 и 482 пикселей."
                )
        return title_photo
