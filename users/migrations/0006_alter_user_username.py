# Generated by Django 4.1.3 on 2023-02-14 13:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_alter_user_email_alter_user_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                help_text="\n        Обязательное поле. Не более 10 символов.\n        только буквы, цифры и символы @/./+/-/_.\n        ",
                max_length=10,
                unique=True,
                verbose_name="Имя пользователя",
            ),
        ),
    ]
