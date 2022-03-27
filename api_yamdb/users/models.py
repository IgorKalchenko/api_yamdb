from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

CHOICES = (
        ('USER', 'Аутентифицированный пользователь'),
        ('MODERATOR', 'Модератор'),
        ('ADMIN', 'Администратор'),
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
        default='USER'
    )
    @property
    def is_admin(self):
        return self.role == 'ADMIN' or self.is_staff

    @property
    def is_moderator(self):
        return self.role == 'MODERATOR'



# class Role(models.TextChoices):
#     USER = 'user',
#     MODERATOR = 'moderator'
#     ADMIN = 'admin'