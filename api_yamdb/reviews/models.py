import datetime as dt
from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Жанр'
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
    
    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        # unique=True, - в разных категориях могут повторяться
        max_length=256
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
        validators=[MaxValueValidator(dt.datetime.today().year)]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles'
        )
    genre = models.ManyToManyField(Genre, through='Genre_Title')

    class Meta:
        verbose_name = 'Наименование'
        verbose_name_plural = 'Наименования'

    def __str__(self):
        return self.name


class Genre_Title(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f'{self.title} {self.genre}'

# class Review(models.Model):
#     title = models.ForeignKey(
#         Title,
#         on_delete=models.CASCADE
#     )
#     text = models.TextField()
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE
#     )
#     score = models.PositiveSmallIntegerField(
#         validators=[MinValueValidator(0),
#                     MaxValueValidator(10)]
#     )
#     pub_date = models.DateTimeField(
#         verbose_name='Дата публикации',
#         auto_now_add=True,
#         db_index=True
#     )

#     class Meta:
#         ordering = ['-pub_date']
#         verbose_name = 'Отзыв'
#         verbose_name_plural = 'Отзывы'


# class Commentary(models.Model):
#     review = models.ForeignKey(
#         Review, 
#         on_delete=models.CASCADE,
#     )
#     text = models.TextField(
#         null=True,
#         blank=True
#     )
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE)
#     pub_date = models.DateTimeField(
#         verbose_name='Дата публикации',
#         auto_now_add=True,
#         db_index=True
#     )

#     class Meta:
#         verbose_name = 'Комментарий'
#         verbose_name_plural = 'Комментарии'
