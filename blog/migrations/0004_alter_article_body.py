# Generated by Django 4.1.3 on 2023-02-15 09:06

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0003_alter_article_title_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="body",
            field=tinymce.models.HTMLField(verbose_name="Содержание"),
        ),
    ]
