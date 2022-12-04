from django.contrib import admin

from blog.models import Language, Article, Tag


admin.site.register(Tag)
admin.site.register(Language)
admin.site.register(Article)
