from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        "Уникальный логин",
        max_length=150,
        unique=True,
        db_index=True,
    )
    first_name = models.CharField("Имя", max_length=150, null=True)
    last_name = models.CharField("Фамилия", max_length=150, null=True)
    email = models.EmailField(
        "Адрес электронной почты",
        max_length=254,
        unique=True,
        db_index=True,
    )
    follow = models.ManyToManyField(
        verbose_name="Подписка",
        related_name="followers",
        to="self",
        symmetrical=False,
        db_index=True,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("username",)

    def __str__(self):
        return self.username
