from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from blog.models import Blog


class User(AbstractUser):
    """Модель представляющая зарегистрированного пользователя."""
    def __str__(self):
        return self.get_username()

    class Meta:
        ordering = ['-date_joined']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about_me = models.TextField('О себе', null=True)
    blogs = models.ManyToManyField(Blog, verbose_name='Следит за данными тегами', blank=True)

    def __str__(self):
        return self.user.get_username()
