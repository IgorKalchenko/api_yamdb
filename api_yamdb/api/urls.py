from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, GenreViewSet,
                    TitleViewSet)


router = DefaultRouter()
router.register(r'titles', TitleViewSet, basename='title')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'genres', GenreViewSet, basename='genre')

urlpatterns = [
    path('v1/', include(router.urls)),
]