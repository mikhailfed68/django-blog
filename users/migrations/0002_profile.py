# Generated by Django 4.1.3 on 2023-02-03 17:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_article'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to=users.models.get_user_directory_path, verbose_name='Фото профиля')),
                ('about_me', models.CharField(blank=True, max_length=60, null=True, verbose_name='О себе')),
                ('blogs', models.ManyToManyField(blank=True, to='blog.blog', verbose_name='Следит за данными блогами')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
