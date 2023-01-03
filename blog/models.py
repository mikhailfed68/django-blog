from django.db import models
from django.urls import reverse
from django.conf import settings

from PIL import Image

from blog.services.blog import get_default_language, get_user_directory_path


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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
        "Make 'title_photo' into a thumbnail if it is not blank, no larger than the given size."
        super().save(*args, **kwargs)

        if self.title_photo:
            img = Image.open(self.title_photo.path)
            MAX_SIZE = (500, 200)
            img.thumbnail(MAX_SIZE)
            img.save(self.title_photo.path)

    class Meta:
        ordering = ['-created_at']


class Blog(TimeStampedModel):
    name = models.CharField('Название', max_length=100, unique=True)
    description = models.CharField('Описание', max_length=256)

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
