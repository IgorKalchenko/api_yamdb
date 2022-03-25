from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb import settings
from .models import User
from .serializers import (MeSerializer, AdminUserSerializer,
ConfirmationCodeSerializer, JWTTokenSerializer)
from .permissions import IsMe


@api_view(['POST'])
def send_confirmation_code(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        send_mail(
            'Код подтверждения',
            f'Ваш код подтверждения: {confirmation_code}',
            settings.DEFAULT_FROM_EMAIL,
            user.email,
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = JWTTokenSerializer(data=request.data, partial=True)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        user = get_object_or_404(
            User, username=username
        )
        confirmation_code = serializer.validated_data.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            resp = {'token': token}
            return Response(data=resp, status=status.HTTP_200_OK)
        message = 'Обязательное поле "confirmation_code" некорректно'
        resp = {'confirmation_code': message}
        return Response(data=resp, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.SearchFilter, )
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
        user = get_object_or_404(User, username=request.user.username)
        if request.method == 'PATCH':
            serializer = MeSerializer(user, data=request.data, partial=True)
            if serializer.is_valid:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
        serializer = MeSerializer(user, partial=True)
        return Response(serializer.data, tatus=status.HTTP_200_OK)
