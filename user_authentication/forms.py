from user_authentication.models import CustomUser
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django import forms


class CustomUserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "password1", "password2"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "data-bs-toggle": "popover",
            "data-bs-trigger": "hover focus",
            "data-bs-placement": "right",
            "title": "Password Requirements",
            "data-bs-content": (
                "• Can’t be too similar to your personal info\n"
                "• At least 8 characters\n"
                "• Not a common password\n"
                "• Not entirely numeric"
            )
        })



class CustomLoginForm(AuthenticationForm):
    pass        



class CustomLogoutForm(forms.Form):
    pass