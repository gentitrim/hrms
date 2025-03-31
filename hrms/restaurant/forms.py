from django.forms import ModelForm # type: ignore
from .models import Order


class CancelOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']


# class CategoryCreateForm(ModelForm):
#     class Meta:
#         model = Categories
#         fields = '__all__'
    



# class ProductCreateForm(ModelForm):
#     class Meta:
#         model = Products
#         fields = '__all__'
 
    


        
