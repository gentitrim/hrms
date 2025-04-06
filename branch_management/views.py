from django.shortcuts import render
from .models import Branch,Product,Categorie,BranchStaff
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import TemplateView,ListView ,FormView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy

class DashboardView(TemplateView):
    template_name = 'manager_dashboard.html'
    login_url = reverse_lazy('login')
    redirect_field_name = "next"

class CreateProductView(CreateView):
    model = Product
    template_name = 'create_product.html'
    fields = '__all__'
    success_url = reverse_lazy('create-product')

    def form_valid(self, form):
        form.instance.branch = self.request.user.branch 
        return super().form_valid(form)
    
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(branch=self.request.user.branch)
    
class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'update_product.html'
    fields = '__all__'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        return Product.objects.filter(branch=self.request.user.branch)
    
class ProductDeleteView(DeleteView):    
    model = Product
    template_name = 'delete_product.html'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        return Product.objects.filter(branch=self.request.user.branch)
    
class CreateCategoryView(CreateView):
    model = Categorie
    template_name = 'create_category.html'
    fields = '__all__'
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        form.instance.branch = self.request.user.branch 
        return super().form_valid(form)
    
class CategoryListView(ListView):
    model = Categorie
    template_name = 'category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Categorie.objects.filter(branch=self.request.user.branch)
    
class CategoryUpdateView(UpdateView):
    model = Categorie
    template_name = 'update_category.html'
    fields = '__all__'
    success_url = reverse_lazy('category_list')

    def get_queryset(self):
        return Categorie.objects.filter(branch=self.request.user.branch)
    
class CategoryDeleteView(DeleteView):
    model = Categorie
    template_name = 'delete_category.html'
    success_url = reverse_lazy('category_list')

    def get_queryset(self):
        return Categorie.objects.filter(branch=self.request.user.branch)
    
    
    

    
