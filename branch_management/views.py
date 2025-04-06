from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import BranchStaff
from main_management.models import Branch
from .forms import CreateBranchStaff
from django.views.generic import ListView,CreateView
from user_authentication.models import CustomUser
from user_authentication.forms import CustomUserRegisterForm
from django.urls import reverse_lazy

class EmployeeCreateView(CreateView):
    template_name = 'branch_management/create_employee.html'
    success_url = reverse_lazy('employee_list')  # Redirect to the employee list after successful creation
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


def update_employee(request, id):
    employee = get_object_or_404(BranchStaff, id=id,)
    if request.method == 'POST':
        form = CreateBranchStaff(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee successfully created!')
            return redirect('employee_list')
    else:
        form = CreateBranchStaff(instance=employee)
    return render(request, 'branch_management/update_employee.html', {'form': form, 'employee': employee})

def delete_employee(request, id):
    employee = get_object_or_404(BranchStaff, id=id, branch=request.user.branch)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee successfully deleted!')
        return redirect('employee_list')
    return render(request, 'branch_management/delete_employee.html', {'employee': employee})

def manager_dashboard(request):
    return render(request, 'branch_management/manager_dashboard.html')
