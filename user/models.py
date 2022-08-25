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

    def __str__(self):
        return self.username
