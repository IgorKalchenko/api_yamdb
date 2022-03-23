from api.permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins
from rest_framework.viewsets import GenericViewSet
from reviews.models import Category, Genre, Title

from .filters import TitleFilter
from .serializers import (CategorySerializer, GenreSerializer,
                          TitlePostSerializer, TitleSerializer)


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    """
    get: /categories/
    Получить список всех категорий
    Права доступа: **Доступно без токена**
    - Поиск по названию категории
    
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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    """
    get: /genres/
    Получить список всех жанров.
    Права доступа: **Доступно без токена**
    - Поиск по названию жанра
    
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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):
    """
    get: /titles/
    Получить список всех объектов.
    Права доступа: **Доступно без токена**
    - фильтрует по полю slug категории
    - фильтрует по полю slug жанра
    - фильтрует по названию произведения
    - фильтрует по году
    
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
    filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('genre', 'category', 'year', 'name',)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer

        return TitlePostSerializer
 