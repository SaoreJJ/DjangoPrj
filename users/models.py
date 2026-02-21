from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Кастомный менеджер для модели User, где email используется вместо username"""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Создает и сохраняет пользователя с заданным email и паролем"""
        if not email:
            raise ValueError('Email должен быть указан')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Создает обычного пользователя"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Создает суперпользователя"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # Убираем поле username

    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('Введите email')
    )

    avatar = models.ImageField(
        upload_to='users/avatars/',
        verbose_name=_('Аватар'),
        blank=True,
        null=True,
        help_text=_('Загрузите аватар')
    )

    phone = models.CharField(
        max_length=20,
        verbose_name=_('Телефон'),
        blank=True,
        null=True,
        help_text=_('Введите номер телефона')
    )

    country = models.CharField(
        max_length=100,
        verbose_name=_('Страна'),
        blank=True,
        null=True,
        help_text=_('Введите страну')
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Пустой список

    objects = UserManager()  # Используем кастомный менеджер

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.email