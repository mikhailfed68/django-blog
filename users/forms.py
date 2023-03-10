from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django_select2 import forms as s2forms

from blog.forms import BlogsWidget

from .models import User


class AuthorsWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "username__icontains",
        "first_name__icontains",
        "last_name__icontains",
    ]


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]


class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "profile_picture",
            "about_me",
            "blogs",
            "following",
        ]
        widgets = {
            "blogs": BlogsWidget,
            "following": AuthorsWidget,
        }

    def clean_profile_picture(self):
        picture = self.cleaned_data.get("profile_picture", False)
        if picture:
            width, height = get_image_dimensions(picture)
            if (width < 150) or (height < 150):
                raise ValidationError(
                    """
                    Слишком маленькое изображение,
                    минимальная высота и ширина - 150 пикселей.
                    """
                )
            elif (width > 1980) or (height > 1080):
                raise ValidationError(
                    """
                    Слишком большое изображение,
                    максимальная высота и ширина - 1980 и 1080 пикселей.
                    """
                )
        return picture
