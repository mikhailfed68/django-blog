from django.db import models
from django.conf import settings

from blog.services.blog import get_default_language


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Article(TimeStampedModel):
    title = models.CharField('Заголовок', max_length=256, unique=True)
    body = models.TextField('Содержание', unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор', on_delete=models.CASCADE)
    language = models.ForeignKey('Language', verbose_name='Язык', on_delete=models.SET(get_default_language))
    tags = models.ManyToManyField('Tag', verbose_name='Теги', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Tag(models.Model):
    name = models.CharField('Тег', max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Language(models.Model):
    language = models.CharField(max_length=16, unique=True, default='Others')

    def __str__(self):
        return self.language
