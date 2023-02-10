from django import forms
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django_select2 import forms as s2forms

from blog.models import Article


class LanguageWidget(s2forms.ModelSelect2Widget):
    search_fields = ["language__icontains"]


class BlogsWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__icontains",
        "description__icontains",
    ]


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "description", "title_photo", "body", "language", "blogs"]
        widgets = {
            "language": LanguageWidget,
            "blogs": BlogsWidget,
        }

    def clean_title_photo(self):
        title_photo = self.cleaned_data.get("title_photo")

        if title_photo:
            width, height = get_image_dimensions(title_photo)
            if (width < 619) or (height < 349):
                raise ValidationError(
                    """
                    Слишком маленькое изображение,
                    минимальная высота и ширина - 619 и 349 пикселей.
                    """
                )
            elif (width > 1980) or (height > 1080):
                raise ValidationError(
                    """Слишком большое изображение,
                    максимальная высота и ширина - 1980 и 1080 пикселей.
                    """
                )
        return title_photo
