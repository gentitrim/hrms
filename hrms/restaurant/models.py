from django.db import models

# Create your models here.
class Staff(models):
    pass

class Categories(models):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
    

class Products(models):
    category_id = models.ForeignKey("Categories",on_delete=models.CASCADE)
    name = models.CharField(max_length=128) 
    ingredients = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return self.name

class Order_item(models):
    product_id = models.ForeignKey('Products',on_delete=models.CASCADE)
    order_id = models.ForeignKey('Order',on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()

class Order(models):
    staff_id = models.ForeignKey('Staff',on_delete=models.DO_NOTHING)
    order_time = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField()

class Shift(models):
    pass