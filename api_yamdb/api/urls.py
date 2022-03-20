from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    CategoryViewSet, GenreViewSet,
    TitleViewSet, CommentViewSet, ReviewViewSet
)

app_name = 'api'
router = SimpleRouter()

router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register('comments', CommentViewSet, basename='comments')
router.register('reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
