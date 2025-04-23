from django.shortcuts import render,redirect,get_object_or_404
# from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Branch
from branch_management.models import BranchStaff
from user_authentication.models import CustomUser
from user_authentication.forms import CustomUserRegisterForm
from .forms import BranchForm,ManagerForm
from django.views.generic import TemplateView,ListView ,FormView, DeleteView,CreateView,UpdateView,DetailView,View
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from hrms.rolemixin import RoleAccessMixin
from restaurant.models import Order
from django.db.models import Sum,Count
# Create your views here.
class OwnerDashboardView(TemplateView):
    model = Branch
    template_name = 'management/owner_dashboard.html'
    allowed_roles = ['admin']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the total number of branches
        context['total_branches'] = Branch.objects.count()
        # Get the total number of managers
        context['total_managers'] = BranchStaff.objects.filter(role='manager').count()
        # Get the total number of staff
        context['total_staff'] = BranchStaff.objects.filter(role = 'staff').count()
        # Get the total number of orders
        context['total_orders'] = Order.objects.count()
        # Get the total revenue
        total = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
        context['total_revenue'] = total / 100

        return context
    
    
class OrdersPerBranchView(TemplateView):
    model = Order
    template_name = 'management/orders_per_branch.html'
    alloewd_roles = ['admin' ]
    context_object_name = 'branches'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the total number of branches
        # Get the branch names
        context['branch_names'] = Branch.objects.values_list('name', flat=True)
        # Get the total number of managers
        context['total_managers'] = BranchStaff.objects.filter(role='manager').count()
        # Get the total number of staff
        context['total_staff'] = BranchStaff.objects.filter(role = 'staff').count()
        # Get the total number of orders
        context['total_orders'] = Order.objects.count()
        # Get the total revenue
        total = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
        context['total_revenue'] = total / 100
        
        return context 

    
    
    
    
    

   

    

class MainPage(LoginRequiredMixin,RoleAccessMixin,TemplateView):
    allowed_roles = ['admin']
    template_name = 'management/main.html'

    
    
    
class BranchListView(LoginRequiredMixin,RoleAccessMixin,ListView):
    allowed_roles = ['admin']
    paginate_by = 3
    model = Branch
    template_name = 'management/branches_list.html'
    ordering = ['name']
    #context_object_name = 'branches'


class CreateBranchView(LoginRequiredMixin,RoleAccessMixin,FormView):
    allowed_roles = ['admin']
    template_name = 'management/create_branch.html'
    success_url = reverse_lazy('main_management:management_dashboard')
    form_class = BranchForm
    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        try:
            Branch.objects.create(
                name = cleaned_data["name"],
                address = cleaned_data["address"],
                phone = cleaned_data["phone"],
                email = cleaned_data["email"],
            )
            return super().form_valid(form)
        except Exception as e:
            return HttpResponse(f"Error: {e}", status=500)
    def form_invalid(self, form):
        return super().form_invalid(form)
    

class SearchBranchView(LoginRequiredMixin,RoleAccessMixin,ListView):
    allowed_roles = ['admin']
    template_name = 'management/branches_list.html'
    paginate_by = 3
    model = Branch
    context_object_name = 'branches'

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        if search:
            return Branch.objects.filter(Q(name__icontains=search)).order_by('name')
        return Branch.objects.all().order_by('name')
    

class EditBranchView(LoginRequiredMixin,RoleAccessMixin,FormView):
    allowed_roles = ['admin']
    template_name = 'management/edit_branch.html'
    success_url = 'main_management:branch'
    form_class = BranchForm
    
    def form_valid(self, form):
        return super().form_valid(form)
    
class DeleteBranchView(LoginRequiredMixin,RoleAccessMixin,DeleteView):
    allowed_roles = ['admin']
    template_name = 'management/delete_branch.html'
    success_url = 'main_management:branch'

class ManagerManagementView(LoginRequiredMixin,TemplateView):
    def get(self,request):
        return render(request,'management/manage_manager.html')



class ManagerListView(LoginRequiredMixin,RoleAccessMixin,ListView):
    allowed_roles = ['admin']
    model = BranchStaff

    template_name = 'management/manage_manager.html'
    context_object_name = 'managers'
    paginate_by = 5

    def get_queryset(self):
        return BranchStaff.objects.filter(role = 'manager')
    

class CreateManagerView(LoginRequiredMixin,RoleAccessMixin,View):
    allowed_roles = ['admin']
    template_name = 'management/create_manager.html'
    success_url = reverse_lazy('main_management:manager_list')
 
    def get(self, request):
        managerform = ManagerForm()
        userform = CustomUserRegisterForm()
        return render(request, self.template_name, {'managerform': managerform, 'userform': userform})
       
    def post(self, request):
        managerform = ManagerForm(request.POST)
        userform = CustomUserRegisterForm(request.POST)
        if managerform.is_valid() and userform.is_valid():
            user = userform.save(commit=False)
            user.save()
            manager = managerform.save(commit=False)
            manager.user = user
            manager.role = 'manager'
            manager.save()
            messages.success(request, 'Manager created successfully!')
            return redirect(self.success_url)
        

        if managerform.errors:
            messages.error(request,"Please complete in the correct form.")
        if userform.errors:
            messages.error(request,"Please complete in the correct form.")
            return render(request, self.template_name, {'managerform': managerform, 'userform': userform})
            
 
        return render(request, self.template_name, {'manager_errors': managerform.errors,
    'user_errors': userform.errors})
    

class ManagerUpdateView(LoginRequiredMixin,RoleAccessMixin,View):
    allowed_roles = ['admin']
    template_name = 'management/manager_edit.html'
    success_url = reverse_lazy('main_management:manager_list')

    def get(self, request, pk):
        manager = get_object_or_404(BranchStaff, pk=pk)
        managerform = ManagerForm(instance=manager)
        userform = CustomUserRegisterForm(instance=manager.user)
        return render(request, self.template_name, {'managerform': managerform, 'userform': userform, 'manager': manager})
    
    def post(self, request, pk):
        manager = get_object_or_404(BranchStaff, pk=pk)
        managerform = ManagerForm(request.POST, instance=manager)
        userform = CustomUserRegisterForm(request.POST, instance=manager.user)
        if managerform.is_valid() and userform.is_valid():
            user = userform.save()
            manager = managerform.save(commit=False)
            manager.user = user
            manager.save()
            messages.success(request, 'Manager updated successfully!')
            return redirect(self.success_url)
        
        if managerform.errors:
            messages.error(request,"Please complete in the correct form.")
        if userform.errors:
            messages.error(request,"Please complete in the correct form.")
            return render(request, self.template_name, {'managerform': managerform, 'userform': userform})
        return render(request, self.template_name, {'managerform': managerform, 
                                                    'userform': userform, 
                                                    'manager': manager
                                                    })


class ManagerDeleteView(LoginRequiredMixin,RoleAccessMixin,View):
    allowed_roles = ['admin']
    template_name = 'management/manager_delete.html'
    success_url = reverse_lazy('main_management:manager_list')

    def get(self, request, pk):
        manager = get_object_or_404(BranchStaff, pk=pk)
        return render(request, self.template_name, {'manager': manager})

    def post(self, request, pk):
        manager = get_object_or_404(BranchStaff, pk=pk)
        user = manager.user
        manager.delete()
        user.delete()
        messages.success(request, 'Manager deleted successfully!')
        
        return redirect(self.success_url)
    

class ManagerDetailView(LoginRequiredMixin,RoleAccessMixin,DetailView):
    allowed_roles = ['admin']
    model = BranchStaff
    template_name = 'management/manager_detail.html'
    context_object_name = 'manager'

    def get_object(self, queryset=None):
        return get_object_or_404(BranchStaff, id=self.kwargs.get('pk'))
       

    
    

