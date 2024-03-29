# Generated by Django 4.1.3 on 2023-02-10 23:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_profile_following_alter_profile_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                error_messages={"unique": "Электронная почта уже используется."},
                help_text="Почта должна быть уникальной.",
                max_length=254,
                unique=True,
                verbose_name="Электронный адресс",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                help_text="Обязательное поле. Не более 10 символов. Только буквы, цифры и символы @/./+/-/_.",
                max_length=10,
                unique=True,
                verbose_name="Имя пользователя",
            ),
        ),
    ]
