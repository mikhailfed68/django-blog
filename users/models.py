from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель представляющая зарегистрированного пользователя."""
    def __str__(self):
        return self.get_username()

    class Meta:
        ordering = ['-date_joined']
