# Generated by Django 4.1.3 on 2023-02-03 17:16

import blog.models
import blog.services.blog
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Заголовок')),
                ('title_photo', models.ImageField(blank=True, null=True, upload_to=blog.models.get_user_directory_path, verbose_name='Фото')),
                ('description', models.CharField(max_length=100, verbose_name='Описание')),
                ('body', models.TextField(verbose_name='Содержание')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('blogs', models.ManyToManyField(blank=True, to='blog.blog', verbose_name='Блоги')),
                ('language', models.ForeignKey(on_delete=models.SET(blog.services.blog.get_default_language), to='blog.language', verbose_name='Язык')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]