from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Categorie
from .forms import CategoryCreateForm

class CategoryListView(ListView):
    model = Categorie
    template_name = 'branch_management/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(CreateView):
    model = Categorie
    form_class = CategoryCreateForm
    template_name = 'branch_management/category_form.html'
    success_url = reverse_lazy('branch_managment:category-list')


class CategoryUpdateView(UpdateView):
    model = Categorie
    form_class = CategoryCreateForm
    template_name = 'branch_management/category_form.html'
    success_url = reverse_lazy('branch_managment:category-list')

class CategoryDeleteView(DeleteView):
    model = Categorie
    template_name = 'branch_management/category_confirm_delete.html'
    success_url = reverse_lazy('branch_managment:category-list')
