from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=20, default='client')

    groups = models.ManyToManyField(Group, related_name="custom_user_set")
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_set"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
