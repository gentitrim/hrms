from django.forms import ModelForm,Form
from .models import Categories,Products,Order


class CategoryCreateForm(ModelForm):
    class Meta:
        model = Categories
        fields = '__all__'

class ProductCreateForm(ModelForm):
    class Meta:
        model = Products
        fields = '__all__'


class ConfirmOrderForm(ModelForm):
     class Meta:
        model = Order
        fields = '__all__'