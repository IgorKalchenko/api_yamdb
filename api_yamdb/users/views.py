from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb import settings
from .models import User
from .serializers import (MeSerializer, AdminUserSerializer,
                         ConfirmationCodeSerializer, JWTTokenSerializer)
from .permissions import IsMe, IsAdmin

def send_code(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        (user.email,),
        fail_silently=False,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def send_confirmation_code(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    user, created = User.objects.get_or_create(username=username, email=email)
    if created:
        send_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    send_code(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    serializer = JWTTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(
        User, username=username
    )
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user).access_token()
        resp = {'token': token}
        return Response(resp, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=True,
        url_path='me',
        url_name='me',
        permission_classes = (IsMe,)
    )
    def me(self, request):
        user = self.request.user
        serializer = MeSerializer(user, data=request.data, partial=True)
        if request.method == 'PATCH':
            if serializer.is_valid:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)
