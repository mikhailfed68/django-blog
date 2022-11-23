from django.db import models


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


class Article(TimeStampedModel):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=256, unique=True)
    body = models.TextField('Содержание', unique=True)
