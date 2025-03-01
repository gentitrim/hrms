from django.forms import ModelForm
from .models import Categories


class CategoryCreateForm(ModelForm):
    class Meta:
        model = Categories
        fields = '__all__'