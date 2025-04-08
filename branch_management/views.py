from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import BranchStaff
from main_management.models import Branch
from .forms import CreateBranchStaff
from django.views.generic import ListView,CreateView, UpdateView, DeleteView, TemplateView
from user_authentication.models import CustomUser
from user_authentication.forms import CustomUserRegisterForm
from django.urls import reverse_lazy

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