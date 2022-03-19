from django.shortcuts import render
from rest_framework import filters, mixins
from rest_framework.viewsets import GenericViewSet
from .serializers import (
    CategorySerializer,
    TitleSerializer,
    TitlePostSerializer,
    GenreSerializer,
)
from reviews.models import Category, Title, Genre
from api.permissions import IsAdminOrReadOnly

class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    """
    get: /categories/
    Получить список всех категорий
    Права доступа: **Доступно без токена**
    Поиск по названию категории
    
    post: /categories/
    Создать категорию.
    Права доступа: **Администратор.**
    
    delete: /categories/{slug}/
    Удалить категорию.
    Права доступа: **Администратор.**
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    """
    get: /genres/
    Получить список всех жанров.
    Права доступа: **Доступно без токена**
    Поиск по названию жанра
    
    post: /genres/
    Добавить жанр.
    Права доступа: **Администратор**
    
    delete: /genres/{slug}/
    Удалить жанр.
    Права доступа: **Администратор**
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet():
    """
    get: /titles/
    Получить список всех объектов.
    Права доступа: **Доступно без токена**
    фильтрует по полю slug категории
    фильтрует по полю slug жанра
    фильтрует по названию произведения
    фильтрует по году
    
    post: /titles/
    Добавить новое произведение.
    Права доступа: **Администратор**.
    Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего).
    При добавлении нового произведения требуется указать уже существующие категорию и жанр.
    
    get: /titles/{titles_id}/
    Информация о произведении
    Права доступа: **Доступно без токена**
    
    patch: /titles/{titles_id}/
    Обновить информацию о произведении
    Права доступа: **Администратор**

    delete: /titles/{titles_id}/
    Удалить произведение.
    Права доступа: **Администратор**
    """
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
 