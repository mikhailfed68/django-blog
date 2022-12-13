from django.contrib import admin

from blog.models import Language, Article, Blog


admin.site.register(Blog)
admin.site.register(Language)
admin.site.register(Article)
