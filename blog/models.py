from django.db import models

from blog.services.blog_services import get_default_language


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Author(TimeStampedModel):
    first_name = models.CharField('Ваше имя', max_length=16)
    surname = models.CharField('Ваша фамилия', max_length=16)
    alias = models.CharField('Ваш псевдоним', max_length=16, unique=True)
    email = models.EmailField('Ваш адрес электронной почты', unique=True)

    def __str__(self):
        return self.alias


class Language(models.Model):
    language = models.CharField(max_length=16, unique=True, default='Others')

    def __str__(self):
        return self.language

class Article(TimeStampedModel):
    author = models.ForeignKey(Author, verbose_name='Автор', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, verbose_name='Язык', on_delete=models.SET(get_default_language))
    title = models.CharField('Заголовок', max_length=256, unique=True)
    body = models.TextField('Содержание', unique=True)

    def __str__(self):
        return self.title
