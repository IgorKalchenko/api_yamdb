from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from reviews.models import Category, Comment, Genre, Review, Title

from .pagination import ApiPagination
from .permissions import AuthorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleReadSerializer)

# from .permissions import AuthorOrReadOnly


class OnlyForCreateDestroyListViewSet(
        ListModelMixin,
        CreateModelMixin,
        DestroyModelMixin,
        viewsets.GenericViewSet):
    pass


class CategoryViewSet(OnlyForCreateDestroyListViewSet):
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
    permission_classes = (AuthorOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(OnlyForCreateDestroyListViewSet):
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
    permission_classes = (AuthorOrReadOnly, )
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
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
    Нельзя добавлять произведения, которые еще не вышли.
    При добавлении произведения требуется указать из списка категорию и жанр.

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
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    )
    permission_classes = (AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('genre', 'category', 'year', 'name',)
    # filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    get: /<title_id>/reviews/
    Получить список всех отзывов.

    Права доступа: **Доступно без токена**

    post: /<title_id>/reviews/
    Добавить новое произведение.

    Права доступа: **Аутентифицированные пользователи**.
    Пользователь может оставить только один отзыв на произведение.

    get: /<title_id>/reviews/<review_id>/
    Получить отзыв по id для указанного произведения.

    Права доступа: **Доступно без токена**

    patch: /<title_id>/reviews/<review_id>/
    Обновить частично отзыв по id.

    Права доступа: **Автор отзыва, модератор или администратор**.

    delete: /<title_id>/reviews/<review_id>/

    Удалить отзыв по id.
    Права доступа: **Автор отзыва, модератор или администратор**.

    """
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        author = self.request.user
        if Review.objects.filter(title=title, author=author).exists():
            raise exceptions.ValidationError(
                'Запрещено добавление более одного на произведение'
            )
        serializer.save(author=author, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    get: /<title_id>/reviews/<review_id>/comments/
    Получить список всех комментариев к отзыву по id

    Права доступа: **Доступно без токена**

    post: /<title_id>/reviews/<review_id>/comments/
    Добавить новый комментарий для отзыва.

    Права доступа: **Аутентифицированные пользователи**.

    get: /<title_id>/reviews/<review_id>/comments/<comment_id>/
    Получить отзыв по id для указанного произведения.

    Права доступа: **Доступно без токена**

    patch: /titles/<title_id>/reviews/<review_id>/comments/<comment_id>/
    Обновить частично отзыв по id.

    Права доступа: **Автор комментария, модератор или администратор**.

    delete: /titles/<title_id>/reviews/<review_id>/comments/<comment_id>/

    Удалить отзыв по id.
    Права доступа: **Автор комментария, модератор или администратор**.

    """
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, review=review)
