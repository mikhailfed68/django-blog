# Generated by Django 4.1.3 on 2022-12-31 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_article_title_photo_alter_article_blogs_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title_photo',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/', verbose_name='Фото'),
        ),
    ]