from django.db import models
from django.contrib.auth import get_user_model

from blog.services.blog import get_default_language


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Author(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    about_yourself = models.TextField('О себе', null=True)
    tags = models.ManyToManyField('Tag', verbose_name='Следит за данными тегами', blank=True)

    def __str__(self):
        return self.user.get_username()


class Article(TimeStampedModel):
    language = models.ForeignKey('Language', verbose_name='Язык', on_delete=models.SET(get_default_language))
    author = models.ForeignKey(Author, verbose_name='Автор', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', verbose_name='Теги', blank=True)
    title = models.CharField('Заголовок', max_length=256, unique=True)
    body = models.TextField('Содержание', unique=True)

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
