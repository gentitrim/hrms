from django.db import models
from user_authentication.models import CustomUser
from main_management.models import Branch

# Create your models here.
class BranchStaff(models.Model):
    role_choices = (
        ('admin','Admin'),
        ('manager','Manager'),
        ('staff','Staff'),)
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='branchstaff')
    role = models.CharField(max_length=128,choices=role_choices,default='staff')
    created = models.DateTimeField(auto_now_add=True)
    phone =models.CharField(max_length=14,blank=True,default="")
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,related_name='branch')

    
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
    price = models.FloatField()
    description = models.CharField(max_length=250,blank=True,default="")
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,related_name='products')
    # image = models.ImageField()

    def get_price_as_float(self):
        return f'{self.price}'

    def __str__(self):
        return self.name
    
    def update_inventory(self, quantity):
        
        self.quantity -= quantity
        self.save()
        
    
class Shift(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
    ]
    branch = models.ForeignKey('main_management.Branch', on_delete=models.CASCADE, related_name='shifts')
    employee = models.ForeignKey('BranchStaff', on_delete=models.CASCADE, related_name='shifts', limit_choices_to={'role': 'staff'})
    day = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ])
    shift_type = models.CharField(max_length=20, choices=[
        ('Morning (AM)', 'Morning (AM)'),
        ('Afternoon (PM)', 'Afternoon (PM)'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_by = models.ForeignKey('BranchStaff', on_delete=models.SET_NULL, null=True, related_name='created_shifts', limit_choices_to={'role': 'manager'})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.day} - {self.shift_type} ({self.employee.user.username} - {self.branch.name})"

    class Meta:
        verbose_name = "Shift"
        verbose_name_plural = "Shifts"