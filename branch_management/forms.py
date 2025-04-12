from django.forms import ModelForm

from .models import Category,Product,BranchStaff


class CategoryCreateForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        exlude = ['branch']
    

class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CreateBranchStaff(ModelForm):
    class Meta:
        model = BranchStaff
        fields = '__all__'
        exclude = ['user', 'branch']