from django.forms import ModelForm # type: ignore
from .models import Order
from branch_management.models import BranchStaff
from user_authentication.models import CustomUser


class CancelOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']


class UserUpdateForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name'] 

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'form-control'
        })

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return first_name.title()
    
    def clean_last_name(self):
        first_name = self.cleaned_data.get('last_name')
        return first_name.title()


class EmployeeUpdateForm(ModelForm):
    class Meta:
        model = BranchStaff
        fields = '__all__'
        exclude = ['user','role','branch']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
            'class': 'form-control'
        })
 
    def clean_username(self):      
        data = self.cleaned_data["username"]
        return data.lower()
   
    def clean_email(self):  
        data = self.cleaned_data["email"]
        return data.lower()
   
    def clean_phone(self):  
        data = self.cleaned_data["phone"]
        return data.lower()

        
