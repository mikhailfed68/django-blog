# Generated by Django 4.1.3 on 2023-02-14 14:04

import blog.models
from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_article"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="title_photo",
            field=sorl.thumbnail.fields.ImageField(
                blank=True,
                null=True,
                upload_to=blog.models.get_user_directory_path,
                verbose_name="Фото",
            ),
        ),
    ]