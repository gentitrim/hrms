from django.forms import ModelForm # type: ignore
from .models import Branch
from branch_management.models import BranchStaff
from user_authentication.models import CustomUser
import re
from django.core.exceptions import ValidationError
from django import forms
 
 
class BranchForm(ModelForm):
    class Meta:
        model = Branch
        fields = '__all__'

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'form-control'
        })
 
    def clean_name(self):      
        data = self.cleaned_data["name"]
        return data.title()
   
    def clean_address(self):
        address = self.cleaned_data["address"]
        return address.title()
   
    def clean_email(self):  
        data = self.cleaned_data["email"]
        return data.lower()
 
    def clean_phone(self):
        if re.match(r'^\+?\d{0,14}$', self.cleaned_data["phone"]):
            data = self.cleaned_data["phone"]
            return data
        else:
            raise forms.ValidationError("Invalid phone number format.")
 
class ManagerForm(ModelForm):
    class Meta:
        model = BranchStaff
        fields = '__all__'
        exclude = ['user','role']
 
    def clean_username(self):      
        data = self.cleaned_data["username"]
        return data.lower()
   
    def clean_email(self):  
        data = self.cleaned_data["email"]
        return data.lower()
   
    def clean_phone(self):  
        data = self.cleaned_data["phone"]
        return data.lower()
    

class CustomManagerUpdateForm(forms.ModelForm):
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