# Generated by Django 4.1.3 on 2022-12-04 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='about_self',
            new_name='about_yourself',
        ),
    ]
