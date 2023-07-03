from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


USERNAMEVALIDATOR = UnicodeUsernameValidator()

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

USER_ROLES = [
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin')]


class User(AbstractUser):
    username = models.CharField(verbose_name='Пользователь',
                                max_length=20,
                                unique=True,
                                help_text=(
                                    'Не больше 20 символов.'
                                    'Только буквы, цифры и @/./+/-/_'),
                                validators=[USERNAMEVALIDATOR],
                                error_messages={
                                    'unique': ('Пользователь с'
                                               'таким именем уже существует')}
                                )
    email = models.EmailField(verbose_name='email',
                              max_length=254,
                              blank=False,
                              unique=True)
    first_name = models.CharField(verbose_name='Имя',
                                  max_length=150,
                                  blank=True)
    last_name = models.CharField(verbose_name='Фамилия',
                                 max_length=150,
                                 blank=True)
    bio = models.TextField(verbose_name='О себе',
                           blank=True)
    role = models.CharField(verbose_name='Права пользователя',
                            max_length=150,
                            choices=USER_ROLES,
                            default='user')
    confirmation_code = models.SlugField(blank=True)

    def __str__(self):
        return self.username[:20]

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.is_staff or self.role == self.ADMIN
