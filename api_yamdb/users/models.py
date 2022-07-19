from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_USER = 'user'
ROLE_MODERATOR = 'moderator'
ROLE_ADMIN = 'admin'

USER_ROLES = [
    (ROLE_USER, 'User'),
    (ROLE_MODERATOR, 'Moderator'),
    (ROLE_ADMIN, 'Admin'),
]


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=254,
        unique=True,
    )
    bio = models.TextField(
        verbose_name='biography',
        blank=True,
        null=True,
    )
    role = models.CharField(
        verbose_name='user role',
        choices=USER_ROLES,
        default=ROLE_USER,
        max_length=20,
    )
    first_name = models.CharField(
        verbose_name='first name',
        max_length=150,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name='last name',
        max_length=150,
        blank=True,
        null=True,
    )

    REQUIRED_FIELDS = [
        'email',
    ]
