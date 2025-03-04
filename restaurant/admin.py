from django.contrib import admin
from restaurant.models import BranchStaff,Order,Order_item,Categories,Products
# Register your models here.
admin.site.register(BranchStaff)
admin.site.register(Order)
admin.site.register(Order_item)
admin.site.register(Categories)
admin.site.register(Products)