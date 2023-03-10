from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.forms import CustomUserChangeForm
from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    search_fields = ("username",)
    autocomplete_fields = ("groups", "blogs")
    form = CustomUserChangeForm  # adding validation for profile_picture field
