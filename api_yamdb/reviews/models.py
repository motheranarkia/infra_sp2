from datetime import datetime as dt

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


def this_year_is_max_value(value):
    return MaxValueValidator(
        dt.now().year,
        'Нельзя добавить произведение из будущего.'
    )(value)


class Category(models.Model):
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        blank=True,
        validators=[
            MinValueValidator(0, 'Попытка добавить древнее произведение?'),
            this_year_is_max_value,
        ]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(Genre, blank=True)
    description = models.TextField('Описание', blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель для напиcания отзыва, напрямую связанная с моделью Title"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review_title',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review_author',
    )
    text = models.TextField(
        'Текст отзыва',
    )
    score = models.IntegerField(
        'Оценка',
        validators=[
            MinValueValidator(
                1, message='Слишком жестоко, оцените хотя бы на единичку'
            ),
            MaxValueValidator(
                10, message='Слишком щедро, мы больше десятки не заслужили'
            )
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментирования отзыва, напрямую связанная с моделью Review"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        'Текст',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
