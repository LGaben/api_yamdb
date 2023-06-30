from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """Модель категории (типы) произведений."""

    name = models.CharField(
        max_length=100,
        verbose_name='Категоря',
        unique=True
    )
    slug = models.SlugField(
        unique=True,
        max_length=50
    )

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name[:50]


class Genre(models.Model):
    """Модель категории жанров."""

    name = models.CharField(
        max_length=100,
        verbose_name='Жанр',
        unique=True
    )
    slug = models.SlugField(
        unique=True,
        max_length=50
    )

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name[:50]


class Title(models.Model):
    """Модель произведения, к которым пишут отзывы."""

    name = models.CharField(
        max_length=100,
        verbose_name='Категоря',
        unique=True,
        blank=True
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Дата выхода произведения',
        validators=(
            MinValueValidator(0),
            MaxValueValidator(datetime.now().year),
        ),
        blank=True
    )
    description = models.CharField(
        max_length=1000,
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        'Genre',
        related_name='Слаг',
        verbose_name='Жанры произведения',
    )
    category = models.ForeignKey(
        'Category',
        related_name='Слаг',
        verbose_name='Категория произведения',
        on_delete=models.SET_NULL, null=True
    )

    class Meta:
        ordering = ('-year',)

    def __str__(self):
        return self.name
