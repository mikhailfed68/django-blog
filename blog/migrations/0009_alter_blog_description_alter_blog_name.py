# Generated by Django 4.1.3 on 2023-01-03 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_article_description_alter_article_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='description',
            field=models.CharField(max_length=256, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Название'),
        ),
    ]
