from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Category
from .forms import CategoryCreateForm

class CategoryListView(ListView):
    model = Category
    template_name = 'branch_management/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'branch_management/category_form.html'
    success_url = reverse_lazy('branch_managment:category-list')


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'branch_management/category_form.html'
    success_url = reverse_lazy('branch_managment:category-list')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'branch_management/category_confirm_delete.html'
    success_url = reverse_lazy('branch_managment:category-list')
