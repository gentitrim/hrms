from django.db import models

# Create your models here.
class BranchStaff(models.Model):
    # user_id = models.ForeignKey('user',on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    role = models.CharField(max_length=128)
    created = models.DateTimeField()
    # branch = models.ForeignKey('Branches',on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.surname}"

class Categories(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
    

class Products(models.Model):
    category = models.ForeignKey("Categories",on_delete=models.CASCADE)
    name = models.CharField(max_length=128) 
    ingredients = models.TextField()
    price = models.IntegerField()
    # image = models.ImageField()

    def __str__(self):
        return self.name

class Order_item(models.Model):
    product_id = models.ForeignKey('Products',on_delete=models.CASCADE)
    order_id = models.ForeignKey('Order',on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()

class Order(models.Model):
    staff_id = models.ForeignKey('BranchStaff',on_delete=models.DO_NOTHING)
    order_time = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField()

class Shift(models.Model):
    pass