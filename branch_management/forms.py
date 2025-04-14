from django.forms import ModelForm
from django import forms
from .models import Category,Product,BranchStaff


class CategoryCreateForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        exlude = ['branch']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'form-control'
        })
    

class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'form-control'
        })

class CreateBranchStaff(ModelForm):
    class Meta:
        model = BranchStaff
        fields = '__all__'
        exclude = ['user', 'branch']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'form-control'
        })


class ProductForm(forms.ModelForm):
    required_css_class = "form-control"
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity', 'price', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['branch'].initial = self.instance.branch
