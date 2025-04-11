from django.db import models
from user_authentication.models import CustomUser


# Create your models here.
class Branch(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=250, blank=True, default="")
    created = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=14, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    

    def __str__(self):
        return f'{self.name} - {self.address}'
    
