from django.db import models # type: ignore
from branch_management.models import BranchStaff,Product
from main_management.models import Branch

# Create your models here.
class Order_item(models.Model):
    
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField(default=1)
    
    price = models.IntegerField()

    def get_price_as_float(self):
        return f'{self.price/100}'
    
    def update_product_inventory(self):
        """Përditëson inventarin e produktit përkatës"""
        self.product_id.update_inventory(self.quantity)

    def __str__(self):
        return self.product_id.name


class Order(models.Model):
    class OrderStatusChoices(models.TextChoices):
        CONFIRMED = 'CONFIRMED'
        CANCELED = 'CANCELED'
    staff_id = models.ForeignKey(BranchStaff,on_delete=models.DO_NOTHING)
    order_time = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField()
    status = models.CharField(max_length=128,choices= OrderStatusChoices,default=OrderStatusChoices.CONFIRMED)

    def get_price_as_float(self):
        return f'{self.total_price/100}'

    def confirm_order(self):
        """Përditëson statusin dhe inventarin e produktit pas konfirmimit të porosisë"""
        self.status = self.OrderStatusChoices.CONFIRMED
        self.save()

        # Përditësojmë inventarin për secilën porosi
        for item in self.order_items.all():
            item.update_product_inventory()

    def __str__(self):
        return f'Order {self.id}'