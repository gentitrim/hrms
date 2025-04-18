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
    

class CustomUserResetPassForm(forms.Form):
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput,
        min_length=8
    )
     
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
    )

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'form-control'
        })
            
    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get("new_password")
        pw2 = cleaned_data.get("confirm_password")

        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data