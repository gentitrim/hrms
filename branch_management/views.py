from .models import Branch,Product,Category,BranchStaff
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from branch_management.forms import ProductCreateForm,CategoryCreateForm
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateBranchStaff
from user_authentication.forms import CustomUserRegisterForm

class DashboardView(TemplateView):
    template_name = 'manager_dashboard.html'
    login_url = reverse_lazy('login')
    redirect_field_name = "next"

class CreateProductView(CreateView):
    model = Product
    template_name = 'create_product.html'
    form_class = ProductCreateForm
    # fields = '__all__'
    success_url = reverse_lazy('create-product')
    # context_object_name = 'products'

    def form_valid(self, form):
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


class EmployeeCreateView(CreateView):
    template_name = 'branch_management/create_employee.html'
    success_url = reverse_lazy('employee_list')
    def get(self, request, *args, **kwargs):
        user_create_form = CustomUserRegisterForm()
        branchstaff_form = CreateBranchStaff()

        return render(request, self.template_name, {
            'branchstaff_form': branchstaff_form,
            'user_create_form': user_create_form,
        })
    def post(self, request, *args, **kwargs):
        branchstaff_form = CreateBranchStaff(request.POST)
        user_create_form = CustomUserRegisterForm(request.POST)

        if branchstaff_form.is_valid() and user_create_form.is_valid():
            user = user_create_form.save(commit=False)
            user.is_branch_staff = True
            user.save()

            branchstaff = branchstaff_form.save(commit=False)
            branchstaff.user = user 
            branchstaff.branch = Branch.objects.get(branch_manager__user_id=request.user.id)
            
            branchstaff.save()
            
            messages.success(request, 'Employee successfully created!')
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'branchstaff_form': branchstaff_form,
            'user_create_form': user_create_form,
        })
    

class EmployeeListView(ListView):
    model = BranchStaff
    template_name = 'branch_management/employee_list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        branch = Branch.objects.filter(branch_manager__user_id=self.request.user.id).first()
        if branch:
            return BranchStaff.objects.filter(branch=branch)
        return BranchStaff.objects.none()


class UpdateEmployeeView(UpdateView):
    model = BranchStaff
    form_class = CreateBranchStaff
    template_name = 'branch_management/update_employee.html'
    context_object_name = 'employee'
    pk_url_kwarg = 'id'
    
    def get_success_url(self):
        messages.success(self.request, 'Employee successfully updated!')
        return reverse_lazy('branch_management:employee_list')

class DeleteEmployeeView(DeleteView):
    model = BranchStaff
    template_name = 'branch_management/delete_employee.html'
    context_object_name = 'employee'
    success_url = reverse_lazy('branch_management:employee_list')

    def get_queryset(self):
        from main_management.models import Branch
        try:
            branch = Branch.objects.get(branch_manager__user=self.request.user)
            return BranchStaff.objects.filter(branch=branch)
        except Branch.DoesNotExist:
            return BranchStaff.objects.none()

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(self.request, "Employee successfully deleted!")
        return response
    
    
class ManagerDashboardView(TemplateView):
    template_name = 'branch_management/manager_dashboard.html'



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