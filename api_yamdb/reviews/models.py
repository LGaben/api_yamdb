from django.db import models
from users.models import User
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
        on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ('-year',)

    def __str__(self):
        return self.name[:50]


class Feedback(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s',
    )
    text = models.TextField(
        max_length=500,
        verbose_name='Текст отзыва',
        help_text='Введите текст отзыва'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ['pub_date']

    def __str__(self):
        return self.text[:50]


class Review(Feedback):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=(MinValueValidator(1, 'Оценка должна быть от 1 до 10'),
                    MaxValueValidator(10, 'Оценка должна быть от 1 до 10'))
    )

    class Meta(Feedback.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review'
            ),
        ]


class Comment(Feedback):
    review = models.ForeignKey(
        Review,
        verbose_name='Комментарии',
        on_delete=models.CASCADE,
        related_name='comments',
        blank=True,
        null=True
    )

    class Meta(Feedback.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
