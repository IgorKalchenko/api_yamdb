from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    CHOICES = [
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]
    email = models.EmailField(
        _('email address'),
        unique=True,
        blank=False,
        max_length=254
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    bio = models.TextField(
        _('biography'),
        blank=True,
        null=True
    )
    role = models.CharField(
        _('role'),
        max_length=max(len(choice) for choice, _ in CHOICES),
        choices=CHOICES,
        default=USER
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
