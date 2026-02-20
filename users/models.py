from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email должен быть задан")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser должен иметь is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Кастомный пользователь.
    Логин = email.
    Доп. поля: avatar, phone_number, country.
    """

    username = None
    email = models.EmailField("Email", unique=True)

    avatar = models.ImageField("Аватар", upload_to="avatars/", blank=True, null=True)
    phone_number = models.CharField("Номер телефона", max_length=20, blank=True)
    country = models.CharField("Страна", max_length=100, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email