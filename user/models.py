from django.contrib.auth.models import AbstractUser
from django.db import models

from user.validators import phone_validator


class User(AbstractUser):
    """Модель пользователя"""
    phone = models.CharField('телефон', validators=[phone_validator], max_length=13, unique=True)

    def __str__(self):
        return self.username
