from django.forms import ModelForm

from .models import Categorie,Product,BranchStaff


class CategoryCreateForm(ModelForm):
    class Meta:
        model = Categorie
        fields = '__all__'
    

class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CreateBranchStaff(ModelForm):
    class Meta:
        model = BranchStaff
        fields = '__all__'