from django.forms import ModelForm # type: ignore
from .models import Order
from branch_management.models import BranchStaff


class CancelOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']


class EditProfileForm(ModelForm):
    class Meta:
        model = BranchStaff
        fields = '__all__'
        exclude = ['user', 'branch', 'role', 'is_active', 'is_staff', 'is_superuser']
        
        def __init__(self,*args, **kwargs):
            super().__init__(*args, **kwargs)

            for field in self.fields.values():
                field.widget.attrs.update({
                'class': 'form-control'
            })



    


        
