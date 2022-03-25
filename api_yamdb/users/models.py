from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

CHOICES = (
        ('user', 'Аутентифицированный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )


class User(AbstractUser):
    email = models.EmailField(
        _('email address'), unique=True, blank=False, null=False
    )
    bio = models.TextField(
        _('biography'),
        blank=True,
    )
    role = models.CharField(
        _('role'),
        max_length=50,
        choices=CHOICES,
        default=('user', 'Аутентифицированный пользователь')
    )
    # confirmation_code = models.CharField(
    #     _('confirmation_code'),
    #     max_length=80,
    # )
    # REQUIRED_FIELDS = ['email', 'username']
