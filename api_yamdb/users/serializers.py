from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class MeSerializer(serializers.ModelSerializer):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    CHOICES = [
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]
    role = serializers.ChoiceField(read_only=True, choices=CHOICES, default=USER)
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Поле "username" должно быть уникальным'
        )]
    )
    email=serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Поле "email" должно быть уникальным'
        )]
    )

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Поле "username" не может иметь значение "me".'
            )
        return value


class AdminUserSerializer(MeSerializer):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    CHOICES = [
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]
    role = serializers.ChoiceField(read_only=False, choices=CHOICES, default=USER)


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Поле "username" должно быть уникальным'
        )]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Поле "email" должно быть уникальным'
        )]
    )
    confirmation_code = serializers.CharField(required=False, max_length=150)
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Поле "username" не может иметь значение "me".'
            )
        return value


class JWTTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(max_length=150)
    

