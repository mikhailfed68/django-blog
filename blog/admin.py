from django.contrib import admin

from blog.models import Language, Article, Blog


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'author', 'updated_at', 'created_at')
    search_fields = ('title',)
    search_help_text = 'Начните поиск по заголовкам'
    list_filter = ('created_at', 'updated_at')
    list_per_page = 20

    exclude = ('author',)
    autocomplete_fields = ('author', 'language', 'blogs')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    search_fields = ('name',)
