from .models import Branch,Product,Category,BranchStaff
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DeleteView,View
from django.urls import reverse_lazy
from branch_management.forms import ProductCreateForm,CategoryCreateForm,CreateBranchStaff,CustomUserUpdateForm
from user_authentication.models import CustomUser
from user_authentication.forms import CustomUserResetPassForm
from django.contrib import messages
from user_authentication.forms import CustomUserRegisterForm
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from hrms.rolemixin import RoleAccessMixin
from restaurant.models import Order
from django.db.models import Sum


class DashboardView(LoginRequiredMixin,RoleAccessMixin,View):
    allowed_roles = ['manager']
    login_url = reverse_lazy('login')
    redirect_field_name = "next"
    def get(self, request, *args, **kwargs):
        user_branch = self.request.user.branchstaff.branch
        staff = BranchStaff.objects.filter(branch=user_branch).exclude(user=self.request.user)       
        orders = Order.objects.filter(staff_id__branch__id=user_branch.id)
        print(orders)
        total_amount = orders.filter(status='CONFIRMED').aggregate(Sum('total_price'))['total_price__sum'] or 0
        context = {
            'orders': orders,
            'total_amount': total_amount / 100,
            'total_orders': orders.count() or 0,
            'staff_number': staff.count() or 0,
        }
        return render(request, 'manager_dashboard.html', context)



# Product Views

class CreateProductView(LoginRequiredMixin,RoleAccessMixin,CreateView):
    allowed_roles = ['manager']
    model = Product
    template_name = 'create_product.html'
    form_class = ProductCreateForm
    success_url = reverse_lazy('branch_management:create-product')

    def get(self, request, *args, **kwargs):
        product_create_form = ProductCreateForm()
        # Filter categories based on the user's branch
        product_create_form.fields['category'].queryset = Category.objects.filter(branch=request.user.branchstaff.branch)
        return render(request, self.template_name, {
            'product_create_form': product_create_form
        })   
           
    def post(self, request, *args, **kwargs):
        product_create_form = ProductCreateForm(request.POST)
        if product_create_form.is_valid():
            product = product_create_form.save(commit=False)
            product.branch = Branch.objects.get(branch__user_id=request.user.id)
            product.save()
            
            messages.success(request, 'Product successfully created!')
            return redirect(self.success_url)

        # Ensure the category field is filtered again in case of form errors
        product_create_form.fields['category'].queryset = Category.objects.filter(branch=request.user.branchstaff.branch)
        return render(request, self.template_name, {
            'product_create_form': product_create_form,
        })


class ProductListView(LoginRequiredMixin,RoleAccessMixin,ListView):
    allowed_roles = ['manager']
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        user_branch = self.request.user.branchstaff.branch
        return Product.objects.filter(branch=user_branch)   
    

class ProductUpdateView(LoginRequiredMixin,RoleAccessMixin,UpdateView):
    allowed_roles = ['manager']
    model = Product
    form_class = ProductCreateForm
    template_name = 'update_product.html'
    context_object_name = 'products'
    success_url = reverse_lazy('branch_management:product-list')
    

    def get_queryset(self):
        user_branch = self.request.user.branchstaff.branch
        return Product.objects.filter(branch=user_branch) 
    

class ProductDeleteView(LoginRequiredMixin,RoleAccessMixin,DeleteView): 
    allowed_roles = ['manager']
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('branch_management:product-list')

    def get_queryset(self):
        user_branch = self.request.user.branchstaff.branch
        return Product.objects.filter(branch=user_branch) 



# Employee Views

class EmployeeCreateView(LoginRequiredMixin,RoleAccessMixin,CreateView):
    allowed_roles = ['manager']
    template_name = 'branch_management/create_employee.html'
    success_url = reverse_lazy('branch_management:employee-list')
    
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

            branchstaff = branchstaff_form.save(commit=False)
            branchstaff.user = user 
            branchstaff.branch = Branch.objects.get(branch__user_id=request.user.id)
            branchstaff.role = 'staff'
            user.save()
            branchstaff.save()
            
            messages.success(request, 'Employee successfully created!')
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'branchstaff_form': branchstaff_form,
            'user_create_form': user_create_form,
        })   


class EmployeeListView(LoginRequiredMixin,RoleAccessMixin,ListView):
    allowed_roles = ['manager']
    model = BranchStaff
    template_name = 'branch_management/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10

    def get_queryset(self):
        branch = Branch.objects.filter(branch__user_id=self.request.user.id).first()
        if branch:
            return BranchStaff.objects.filter(branch=branch).exclude(user=self.request.user)
        return BranchStaff.objects.none()


class UpdateEmployeeView(LoginRequiredMixin,RoleAccessMixin,UpdateView):
    allowed_roles = ['manager']
    model = BranchStaff
    form_class = CreateBranchStaff
    template_name = 'branch_management/update_employee.html'
    context_object_name = 'employee'
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        staff_form = self.form_class(instance=self.object)
        user_form = CustomUserUpdateForm(instance=self.object.user)
        return render(request, self.template_name, {
            'staff_form': staff_form,
            'user_form': user_form
        })
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        staff_form = self.form_class(request.POST, instance=self.object)
        user_form = CustomUserUpdateForm(request.POST, instance=self.object.user)
        if staff_form.is_valid() and user_form.is_valid():
            staff_form.save()
            user_form.save()
            messages.success(request, 'Employee successfully updated!')
            return redirect(self.get_success_url())
        return render(request, self.template_name, {
            'staff_form': staff_form,
            'user_form': user_form
        })

    def get_success_url(self):
        return reverse_lazy('branch_management:employee-list')
    

class EmployeeResetPasswordView(LoginRequiredMixin,RoleAccessMixin,View):
    allowed_roles = ['manager']
    template_name = 'management/reset_password.html'

    def get(self, request, pk):
        staff_user = get_object_or_404(CustomUser, pk=pk)
        form = CustomUserResetPassForm()
        return render(request, self.template_name, {'form': form, 'staff_user': staff_user})

    def post(self, request, pk):
        staff_user = get_object_or_404(CustomUser, pk=pk)
        form = CustomUserResetPassForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            staff_user.set_password(new_password)
            staff_user.save()
            messages.success(request, f"Password for {staff_user.username} has been changed.")
            return redirect('branch_management:employee-list')  # or any page you want
        return render(request, self.template_name, {'form': form, 'staff_user': staff_user})

    

class DeleteEmployeeView(LoginRequiredMixin,RoleAccessMixin,DeleteView):
    allowed_roles = ['manager']
    model = CustomUser
    template_name = 'branch_management/delete_employee.html'
    context_object_name = 'employee'
    success_url = reverse_lazy('branch_management:employee-list')

    def get_queryset(self):
        branch = Branch.objects.filter(branch__user_id=self.request.user.id).first()
        if branch:
            return CustomUser.objects.filter(branchstaff__branch=branch).exclude(id=self.request.user.id)
        return CustomUser.objects.none()

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(self.request, "Employee successfully deleted!")
        return response


class DetailEmployeeView(LoginRequiredMixin,RoleAccessMixin,TemplateView):
    allowed_roles = ['manager']
    template_name = 'branch_management/detail_employee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee_id = self.kwargs.get('pk')
        employee = BranchStaff.objects.get(pk=employee_id)
        context['employee'] = employee
        return context


#Category Views

class CategoryListView(LoginRequiredMixin,RoleAccessMixin,ListView):
    allowed_roles = ['manager']
    model = Category
    template_name = 'branch_management/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_queryset(self):
        user_branch = self.request.user.branchstaff.branch
        return Category.objects.filter(branch=user_branch) 


class CategoryCreateView(LoginRequiredMixin,RoleAccessMixin,CreateView):
    allowed_roles = ['manager']
    template_name = 'branch_management/category_form.html'
    success_url = reverse_lazy('branch_management:category-list')

    def get(self, request, *args, **kwargs):
        category_create_form = CategoryCreateForm()
        print(self.request.user.branchstaff.branch)
        return render(request, self.template_name, {
            'category_create_form': category_create_form,
        })
    
    def post(self, request, *args, **kwargs):
          
        category_create_form = CategoryCreateForm(request.POST)
        if category_create_form.is_valid():
            category = category_create_form.save(commit=False)
            category.branch = Branch.objects.get(branch__user_id = request.user.id)         
            category.save()
            
            messages.success(request, 'Category successfully created!')
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'category_create_form': category_create_form,
        })


class CategoryUpdateView(LoginRequiredMixin,RoleAccessMixin,UpdateView):
    allowed_roles = ['manager']
    model = Category
    form_class = CategoryCreateForm
    template_name = 'branch_management/category_update.html'
    success_url = reverse_lazy('branch_management:category-list')


    def get_queryset(self):
        user_branch = self.request.user.branchstaff.branch
        return Category.objects.filter(branch=user_branch)
    
    def get_success_url(self):
        messages.success(self.request, 'Category successfully updated!')
        return reverse_lazy('branch_management:category-list')


class CategoryDeleteView(LoginRequiredMixin,RoleAccessMixin,DeleteView):
    allowed_roles = ['manager']
    model = Category
    template_name = 'branch_management/category_confirm_delete.html'
    success_url = reverse_lazy('branch_management:category-list')

    def get_queryset(self):
        try:
            branch = Branch.objects.get(branch__user=self.request.user)
            return Category.objects.filter(branch=branch)
        except Category.DoesNotExist:
            return Category.objects.none()
        
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(self.request, "Category successfully deleted!")
        return response
    


# class TotalOrdersView(LoginRequiredMixin,RoleAccessMixin,View):
#     allowed_roles = ['manager']
#     def get(self, request, *args, **kwargs):
#         user_branch = self.request.user.branchstaff.branch
#         orders = get_object_or_404(Order,branch=user_branch)
#         print(orders)
#         total_amount = orders.filter(status='CONFIRMED').aggregate(Sum('total_price'))['total_price__sum'] or 0
#         context = {
#             'orders': orders,
#             'total_amount': total_amount / 100,
#             'total_orders': orders.count() or 0,
#         }
#         return render(request, 'manager_dashboard.html', context)
    