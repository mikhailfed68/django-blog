# Generated by Django 4.1.3 on 2023-02-19 19:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0007_alter_article_language_alter_language_language"),
    ]

    operations = [
        migrations.AlterField(
            model_name="language",
            name="language",
            field=models.CharField(max_length=16, unique=True, verbose_name="Язык"),
        ),
    ]
