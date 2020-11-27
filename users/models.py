from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    bio = models.TextField(
        _('biography'),
        max_length=2000,
        blank=True,
        null=True,
    )
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        _('role'),
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        unique_together = ('email', 'username')

    def __str__(self):
        return self.email

    @property
    def is_moderator(self):
        return self.is_staff or self.role == Role.MODERATOR

    @property
    def is_admin(self):
        return self.is_superuser or self.role == Role.ADMIN
