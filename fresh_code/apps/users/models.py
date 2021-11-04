from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    ADMIN, GENERAL = ('admin', 'user')

    ROLE_STATE_CHOICES = (
        (ADMIN, 'ADMIN'),
        (GENERAL, 'GENERAL'),
    )

    email = models.EmailField(max_length=190, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_STATE_CHOICES, default=GENERAL)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()
