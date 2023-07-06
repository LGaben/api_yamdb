from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from api.validators import validate_username


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

USER_ROLES = [
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin')]


class User(AbstractUser):
    username = models.CharField(verbose_name='Пользователь',
                                max_length=150,
                                unique=True,
                                help_text=(
                                    'Не больше 150 символов.'
                                    'Только буквы, цифры и @/./+/-/_'),
                                validators=[validate_username, UnicodeUsernameValidator()],
                                error_messages={
                                    'unique': ('Пользователь с'
                                               'таким именем уже существует')}
                                )
    email = models.EmailField(verbose_name='email',
                              max_length=254,
                              blank=False,
                              unique=True)
    role = models.CharField(verbose_name='Права пользователя',
                            max_length=150,
                            choices=USER_ROLES,
                            default=USER)
    bio = models.TextField(verbose_name='О себе',
                           blank=True)
    first_name = models.CharField(verbose_name='Имя',
                                  max_length=150,
                                  blank=True)
    last_name = models.CharField(verbose_name='Фамилия',
                                 max_length=150,
                                 blank=True)
    confirmation_code = models.SlugField(blank=True)
    password = False

    def __str__(self):
        return self.username[:150]

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.is_staff or self.role == ADMIN
