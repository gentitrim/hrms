from django.db import models
from user_authentication.models import CustomUser
from main_management.models import Branch

# Create your models here.
class BranchStaff(models.Model):
    role_choices = (
        ('manager','Manager'),
        ('staff','Staff')
    )
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='branchstaff')
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    role = models.CharField(max_length=128,choices=role_choices,default='staff')
    created = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=14, blank=True, default="")
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.surname}"
    
class Category(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=250,blank=True,default="")
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,related_name='categories')
    def __str__(self):
        return self.name

    
class Product(models.Model):
    category = models.ForeignKey("Category",on_delete=models.CASCADE)
    name = models.CharField(max_length=128) 
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    description = models.CharField(max_length=250,blank=True,default="")
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,related_name='products')
    # image = models.ImageField()

    def get_price_as_float(self):
        return f'{self.price/100}'

    def __str__(self):
        return self.name
    
class Shift(models.Model):
    pass