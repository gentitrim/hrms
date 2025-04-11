from django.forms import ModelForm # type: ignore
from .models import Branch
from branch_management.models import BranchStaff


class BranchForm(ModelForm):
    class Meta:
        model = Branch
        fields = '__all__'

    def clean_name(self):
        data = self.cleaned_data["name"]
        return data.title()
        

class ManagerForm(ModelForm):
    class Meta:
        model = BranchStaff
        fields = '__all__'




