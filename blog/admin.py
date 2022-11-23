from django.contrib import admin

from blog.models import Language, Article, Author


admin.site.register(Language)
admin.site.register(Article)
admin.site.register(Author)