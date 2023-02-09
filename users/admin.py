from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.forms import ChangeProfileForm
from users.models import Profile, User


class ProfileInLine(admin.StackedInline):
    model = Profile
    form = ChangeProfileForm  # adding validation for profile_picture field
    verbose_name_plural = "Профили"
    can_delete = False
    max_num = 1
    autocomplete_fields = ("blogs",)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    search_fields = ("useranme",)
    autocomplete_fields = ("groups",)
    inlines = (ProfileInLine,)
