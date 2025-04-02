from django.forms import ModelForm # type: ignore
from .models import Branch,BranchManager


class BranchForm(ModelForm):
    class Meta:
        model = Branch
        fields = '__all__'


class ManagerForm(ModelForm):
    class Meta:
        model = BranchManager
        fields = '__all__'




