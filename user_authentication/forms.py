from user_authentication.models import CustomUser
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django import forms


class CustomUserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "password1", "password2"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fileds in self.fields.values():
            fileds.widget.attrs.update({
                'class':'form-control',
            })

    def clean_username(self):      
        data = self.cleaned_data["username"]
        return data.lower()

    def clean_first_name(self):
        data = self.cleaned_data["first_name"]
        return data.title()
    
    def clean_last_name(self): 
        data = self.cleaned_data["last_name"]
        return data.title()


class CustomLoginForm(AuthenticationForm):
    pass        



class CustomLogoutForm(forms.Form):
    pass