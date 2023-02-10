from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from blog.forms import BlogsWidget

from .models import Profile, User


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


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_picture", "about_me", "blogs"]
        widgets = {
            "blogs": BlogsWidget,
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


class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
