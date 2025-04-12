from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):

    created_by_manager = models.ForeignKey(
        'main_management.BranchManager',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_users'

    )

    class Meta:
        db_table = "custom_user"