# accounts/models.py
#
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False)

    def __str__(self):
        return self.get_full_name() or self.first_name or self.email