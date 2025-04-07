from django.shortcuts import render
from .models import Branch,Product,Categorie,BranchStaff
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import TemplateView,ListView ,FormView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from branch_management.forms import ProductCreateForm,CategoryCreateForm
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class DashboardView(TemplateView):
    template_name = 'manager_dashboard.html'
    login_url = reverse_lazy('login')
    redirect_field_name = "next"

class CreateProductView(CreateView):
    model = Product
    template_name = 'create_product.html'
    fields = '__all__'
    success_url = reverse_lazy('create-product')
    context_object_name = 'products'

    def form_valid(self, form):
        # Seto dega e përdoruesit aktual
        form.instance.branch = self.request.user.branchstaff.branch
        return super().form_valid(form)
        
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Filtroni produktet sipas degës së përdoruesit të lidhur
        user_branch = self.request.user.branchstaff.branch
        return Product.objects.filter(branch=user_branch)



    
    
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'update_product.html'
    context_object_name = 'products'
    success_url = reverse_lazy('product-list')
    

    def get_queryset(self):
        # Filtroni produktet që janë vetëm për degën e përdoruesit
        user_branch = self.request.user.branchstaff.branch
        return Product.objects.filter(branch=user_branch)

    
    
class ProductDeleteView(DeleteView): 
     
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('product-list')




class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity', 'price', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Kjo mund të sigurojë që dega të jetë e vendosur automatikisht nga përdoruesi
        if self.instance and self.instance.pk:
            self.fields['branch'].initial = self.instance.branch


    
    
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
    
    
    

    
