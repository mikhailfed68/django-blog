"""
Django-blog URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Администрирование Incognito"
admin.site.index_title = "Администрирование вашего сайта"
admin.site.site_title = "Административный сайт Incognito"


urlpatterns = [
    path("", include("blog.urls")),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
]

urlpatterns += [
    path("select2/", include("django_select2.urls")),
]

urlpatterns += [
    # 'неявные' view из auth app (шаблоны лежат в /templates/registration)
    path("users/", include("django.contrib.auth.urls")),
    # остальные view и шаблоны пользователей лежат в users app
    path("users/", include("users.urls")),
]

urlpatterns += [
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
    path('__debug__/', include('debug_toolbar.urls')),
]
