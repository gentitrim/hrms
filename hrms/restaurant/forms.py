from django.forms import ModelForm # type: ignore
from .models import Order


class CancelOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']



    


        
