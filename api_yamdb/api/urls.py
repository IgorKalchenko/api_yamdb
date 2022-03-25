from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import AdminUserViewSet, get_jwt_token, send_confirmation_code

router = DefaultRouter()
router.register('users', AdminUserViewSet, basename='users')
urlpatterns = [
    path('', include(router.urls)),
    path('v1/auth/signup/', send_confirmation_code),
    path('v1/api-token-auth/', get_jwt_token)
]