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

    


        
