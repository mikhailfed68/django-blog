from django.db import models
from django.urls import reverse
from django.conf import settings

from blog.services.blog import get_default_language

from common.utils import set_picture


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def get_user_directory_path(instance, filename):
    return f'users/user_{instance.author.id}/article_{instance.id}/{filename}'


class Article(TimeStampedModel):
    "Article of blog."
    title = models.CharField('Заголовок', max_length=100, unique=True)
    title_photo = models.ImageField('Фото', upload_to=get_user_directory_path, blank=True, null=True)
    description = models.CharField('Описание', max_length=100)
    body = models.TextField('Содержание', unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор', on_delete=models.CASCADE)
    language = models.ForeignKey('Language', verbose_name='Язык', on_delete=models.SET(get_default_language))
    blogs = models.ManyToManyField('Blog', verbose_name='Блоги', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        "Turn the 'title_photo' into a specific thumbnail if it isn't blank."
        super().save(*args, **kwargs)
        if self.title_photo:
            set_picture(self.title_photo.path, (771, 482), type='rectangle')

    class Meta:
        ordering = ['-created_at']


class Blog(TimeStampedModel):
    name = models.CharField('Название', max_length=30, unique=True)
    description = models.CharField('Описание', max_length=60)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:articles_by_blog', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['name']


class Language(models.Model):
    language = models.CharField(max_length=16, unique=True, default='Others')

    def __str__(self):
        return self.language
