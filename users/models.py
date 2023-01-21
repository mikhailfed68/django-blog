from datetime import timedelta

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from blog.models import Blog

from common.utils import set_picture


class User(AbstractUser):
    "A user model."
    def __str__(self):
        return self.get_username()
    
    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'username': self.username})

    def last_seen(self):
        return cache.get(f'last_seen_{self.id}')

    def is_online(self):
        last_seen = self.last_seen()
        if last_seen:
            now = timezone.now()
            if now > last_seen + timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            return True 
        return False

    class Meta:
        ordering = ['username']


def get_user_directory_path(instance, filename):
    return f'users/user_{instance.user.id}/profile_picture/{filename}'


class Profile(models.Model):
    "A profile model with a one-to-one relationship to the User for additional fields."
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField('Фото профиля', upload_to=get_user_directory_path, blank=True, null=True)
    about_me = models.CharField('О себе', max_length=60, blank=True, null=True)
    blogs = models.ManyToManyField(Blog, verbose_name='Следит за данными блогами', blank=True)

    def __str__(self):
        return self.user.get_username()

    def save(self, *args, **kwargs):
        "Turn the 'profile_picture' into a specific thumbnail if it isn't blank."
        super().save(*args, **kwargs)
        if self.profile_picture:
            set_picture(self.profile_picture.path, (150, 150), type='square')
