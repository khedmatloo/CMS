from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, Permission
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=150)
    groups = models.ManyToManyField(Group, verbose_name=(
        'groups'), blank=True, related_name="user_set", related_query_name="user",)
    user_permissions = models.ManyToManyField(
        Permission, verbose_name=('user permissions'), blank=True, help_text=('Specific permissions for this user.'), related_name="user_set", related_query_name="user",)
    is_writer = models.BooleanField(default=False)
    date_joined = models.DateField(default=timezone.now)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_ath_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
