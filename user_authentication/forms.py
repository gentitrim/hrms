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
        pass1 = cleaned_data.get("new_password")
        pass2 = cleaned_data.get("confirm_password")

        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data