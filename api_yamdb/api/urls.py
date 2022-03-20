from django.urls import path, include
from rest_framework.routers import SimpleRouter

app_name = 'api'
router = SimpleRouter()

# router.register()


urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
