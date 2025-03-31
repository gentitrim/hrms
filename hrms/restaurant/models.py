from django.db import models # type: ignore
from user_authentication.models import CustomUser


# To transfere to manager app
class BranchStaff(models.Model):
    user_id = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    role = models.CharField(max_length=128)
    created = models.DateTimeField()
    # branch = models.ForeignKey('Branches',on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.surname}"


# To transfere to manager app
class Categories(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
    
# To transfere to manager app
class Products(models.Model):
    category = models.ForeignKey("Categories",on_delete=models.CASCADE)
    name = models.CharField(max_length=128) 
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    description = models.CharField(max_length=250,blank=True,default="")
    # image = models.ImageField()

    def get_price_as_float(self):
        return f'{self.price/100}'

    def __str__(self):
        return self.name
    

class Order_item(models.Model):
    
    product_id = models.ForeignKey('Products',on_delete=models.CASCADE)
    order_id = models.ForeignKey('Order',on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    price = models.IntegerField()

    def get_price_as_float(self):
        return f'{self.price/100}'

    def __str__(self):
        return self.product_id.name


class Order(models.Model):
    class OrderStatusChoices(models.TextChoices):
        CONFIRMED = 'CONFIRMED'
        CANCELED = 'CANCELED'
    staff_id = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING)
    order_time = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField()
    status = models.CharField(max_length=128,choices= OrderStatusChoices,default=OrderStatusChoices.CONFIRMED)

    def get_price_as_float(self):
        return f'{self.total_price/100}'

class Shift(models.Model):
    pass