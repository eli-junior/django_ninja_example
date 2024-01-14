from typing import Any

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str | None = None, password: str | None = None, **extra_fields: Any) -> Any:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email", default="", unique=True)
    name = models.CharField(_("Name"), max_length=255, default="", blank=True)

    is_active = models.BooleanField(_("Active"), default=True)
    is_staff = models.BooleanField(_("Staff"), default=False)
    is_superuser = models.BooleanField(_("Superuser"), default=False)

    date_joined = models.DateTimeField(_("Date Joined"), default=timezone.now)
    last_login = models.DateTimeField(_("Last Login"), blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def get_full_name(self) -> str:
        return self.name

    def get_short_name(self) -> str:
        return self.name or self.email.split("@")[0]

    def __str__(self) -> str:
        return self.email
