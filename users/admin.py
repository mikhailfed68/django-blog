from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User
from blog.models import Author


class AuthorInLine(admin.StackedInline):
    model = Author
    can_delete = False
    verbose_name_plural = 'Авторы'


class UserAdmin(BaseUserAdmin):
    inlines = (AuthorInLine,)


admin.site.register(User, UserAdmin)
