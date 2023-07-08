from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import validate_username


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    USER_ROLES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    ]
    username = models.CharField(
        verbose_name='Пользователь',
        max_length=150,
        unique=True,
        help_text=(
            'Не больше 150 символов.'
            'Только буквы, цифры и @/./+/-/_'
        ),
        validators=[validate_username],
        error_messages={
            'unique': (
                'Пользователь с таким именем или'
                ' с таким емейлом уже существует'
            )
        }
    )
    email = models.EmailField(
        verbose_name='email',
        max_length=254,
        unique=True
    )
    role = models.CharField(
        verbose_name='Права пользователя',
        max_length=150,
        choices=USER_ROLES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True
    )

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.is_staff or self.role == self.ADMIN
