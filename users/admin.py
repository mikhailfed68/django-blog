from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User, Profile


class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профили'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInLine,)


admin.site.register(User, UserAdmin)
