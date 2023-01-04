from django.db import models
from django.contrib.auth.models import AbstractUser

from PIL import Image

from users.services import img
from blog.models import Blog



class User(AbstractUser):
    """Модель представляющая зарегистрированного пользователя."""
    def __str__(self):
        return self.get_username()


def get_user_directory_path(instance, filename):
    """
    Accepts two arguments and returns a Unix-style path
    to be passed along to the storage system.
    """
    return f'users/user_{instance.id}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField('Фото профиля', upload_to=get_user_directory_path, default='default_profile_picture.jpg')
    about_me = models.CharField('О себе', max_length=60, blank=True, null=True)
    blogs = models.ManyToManyField(Blog, verbose_name='Следит за данными блогами', blank=True)

    def __str__(self):
        return self.user.get_username()

    def save(self, *args, **kwargs):
        "Make 'title_photo' into a thumbnail if it is not blank."
        super().save(*args, **kwargs)

        if self.profile_picture:
            with Image.open(self.profile_picture.path) as image:
                image.thumbnail((320, 320), Image.ANTIALIAS)  
                image = img.crop_max_square(image)
                image.save(self.profile_picture.path)
