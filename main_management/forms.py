from django.forms import ModelForm # type: ignore
from .models import Branch
from branch_management.models import BranchStaff
import re
from django.core.exceptions import ValidationError
from django import forms
 
 
class BranchForm(ModelForm):
    class Meta:
        model = Branch
        fields = '__all__'
 
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