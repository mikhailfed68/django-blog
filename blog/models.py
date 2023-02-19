import datetime

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from sorl import thumbnail
from tinymce.models import HTMLField


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        abstract = True


class Blog(TimeStampedModel):
    name = models.CharField("Название", max_length=30, unique=True)
    description = models.CharField("Описание", max_length=60)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:articles_by_blog", kwargs={"pk": self.pk})


class Language(models.Model):
    language = models.CharField("Язык", max_length=16, unique=True)

    def __str__(self):
        return self.language


def get_user_directory_path(instance, filename):
    return f"users/user_{instance.author.id}/article_{instance.id}/{filename}"


class Article(TimeStampedModel):
    "Article of blog."
    title = models.CharField("Заголовок", max_length=100, unique=True)
    title_photo = thumbnail.ImageField(
        "Фото", upload_to=get_user_directory_path, blank=True, null=True
    )
    description = models.CharField("Описание", max_length=100)
    body = HTMLField("Содержание")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Автор", on_delete=models.CASCADE
    )
    language = models.ForeignKey(
        Language, verbose_name="Язык", blank=True, null=True, on_delete=models.SET_NULL
    )
    blogs = models.ManyToManyField(Blog, verbose_name="Блоги", blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:article_detail", kwargs={"pk": self.pk})

    def was_updated_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.updated_at
