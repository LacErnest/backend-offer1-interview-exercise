from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
import datetime
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(unique=True, max_length=20, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True, default="Active")

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
  """Fonction permettant de créer des token à la créaton du user"""
  if created:
    Token.objects.create(user=instance)
