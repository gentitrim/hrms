from user_authentication.models import CustomUser
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django import forms


class CustomUserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "password1", "password2"]



class CustomLoginForm(AuthenticationForm):
    pass        



class CustomLogoutForm(forms.Form):
    pass