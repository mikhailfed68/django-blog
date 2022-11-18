from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Author(TimeStampedModel):
    first_name = models.CharField(max_length=16)
    surname = models.CharField(max_length=16)
    alias = models.CharField(max_length=16, unique=True)
    email = models.EmailField(unique=True)


class Article(TimeStampedModel):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField('Name article', max_length=256)
    body = models.TextField()
