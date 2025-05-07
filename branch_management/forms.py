from django.forms import ModelForm
from django import forms
from .models import Category,Product,BranchStaff
import re
from django.core.exceptions import ValidationError
from user_authentication.models import CustomUser


class CategoryCreateForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ['branch',]

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'form-control'
        })
    def clean_name(self):
        name = self.cleaned_data.get('name')
        return name.title()
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) > 250:
            raise forms.ValidationError("Description is too long.")  
        return description.title()


class ProductCreateForm(ModelForm):
    add_quantity = forms.IntegerField(
        required=False,
        label='Add Quantity',
        widget = forms.NumberInput(attrs={'class': 'form-control'})
    )


    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['branch',]

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'form-control'
        })
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError("Name is too short.")
        return name.title()
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) > 250:
            raise forms.ValidationError("Description is too long.")  
        return description.title()



class CreateBranchStaff(ModelForm):
    class Meta:
        model = BranchStaff
        fields = '__all__'
        exclude = ['user', 'branch' , 'role']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'form-control'
        })

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+?\d{0,14}$', phone):
            raise forms.ValidationError("Invalid phone number format.")
        return phone 
    

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name'] 

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return first_name.title()
    
    def clean_last_name(self):
        first_name = self.cleaned_data.get('last_name')
        return first_name.title()
    

class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = BranchStaff
        fields = ['phone'] 
        exclude = ['branch','role']
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+?\d{0,14}$', phone):
            raise forms.ValidationError("Invalid phone number format.")
        return phone    


    
    