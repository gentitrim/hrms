from django.shortcuts import render,get_object_or_404 # type: ignore
from django.views import View # type: ignore
from django.views.generic import ListView,UpdateView # type: ignore

from django.contrib.auth.mixins import LoginRequiredMixin # type: ignore
from django.db.models import Sum # type: ignore
from django.http import HttpResponseForbidden # type: ignore
import logging
import datetime
from django.contrib import messages # type: ignore

from restaurant.models import Order_item,Order
from restaurant.forms import EmployeeUpdateForm,UserUpdateForm
from branch_management.models import Product,BranchStaff
from hrms.rolemixin import RoleAccessMixin # type: ignore
from user_authentication.models import CustomUser # type: ignore
from django.urls import reverse_lazy # type: ignore


logger = logging.getLogger(__name__)


class ProductsView(LoginRequiredMixin,RoleAccessMixin,ListView):
    allowed_roles = ['staff']
    model = Product
    template_name = 'snippets/product_list_by_category.html'
    context_object_name = 'all_products'

    def get_queryset(self):
        user_branch = self.request.user.branchstaff.branch
        return Product.objects.filter(branch=user_branch,category_id=self.kwargs['pk'])   

class UserOrderListView(LoginRequiredMixin,RoleAccessMixin,ListView):
    allowed_roles = ['staff']
    model = Order
    template_name = 'snippets/my_order_list.html'
    context_object_name = 'orders'
    login_url = 'login'
    redirect_field_name = 'next'
    paginate_by = 10
    def get_queryset(self):
        self.staff = get_object_or_404(BranchStaff,pk = self.request.user.branchstaff.id)
        self.date = self.request.GET.get('search_date') or datetime.date.today()
        return Order.objects.filter(staff_id=self.staff, order_time__date=self.date).order_by('-order_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        selected_date = datetime.date.today()
        total_amount = self.get_queryset().filter(status='CONFIRMED', order_time__date=selected_date).aggregate(Sum('total_price'))['total_price__sum'] or 0
        context['total_amount'] = total_amount / 100

        return context
    

class UserOrderDetailView(LoginRequiredMixin,RoleAccessMixin,View):
    allowed_roles = ['staff']
    def get(self,request,pk):
        staff = get_object_or_404(BranchStaff,pk = self.request.user.branchstaff.id)
        order = get_object_or_404(Order,pk=pk)
        if order.staff_id != staff:
            return HttpResponseForbidden("You are not allowed to view this order.")
        order_items = Order_item.objects.filter(order_id=order)
        context = {
            'order': order,
            'order_items': order_items,
        }
        return render(request, 'snippets/my_order_detail.html', context)
    

class SearchByDate(LoginRequiredMixin,RoleAccessMixin,View):
    allowed_roles = ['staff']
    def get(self,request):
        date = request.GET.get('search_date') or datetime.date.today()
        staff = BranchStaff.objects.get(pk = request.user.id)
        logger.debug(f"Raw request body: {date}")
        orders = Order.objects.filter(order_time__date=date,staff_id=staff).order_by('-order_time')
        order_items = Order_item.objects.filter(order_id__in=orders)
        
        # Calculate total_amount for the selected date
        total_amount = orders.filter(status='CONFIRMED').aggregate(Sum('total_price'))['total_price__sum'] or 0
        
        context = {
            'orders': orders,
            'order_items': order_items,
            'total_amount': total_amount / 100,
        }
        return render(request, 'snippets/my_order_list.html', context)


class StaffProfileView(LoginRequiredMixin,RoleAccessMixin,View):
    allowed_roles = ['staff']
    def get(self,request):
        staff = get_object_or_404(BranchStaff,pk = request.user.branchstaff.id)
        context = {
            'staff': staff,
        }
        return render(request, 'snippets/employee_profile.html', context)
    

class EditProfileView(LoginRequiredMixin,RoleAccessMixin,UpdateView):
    allowed_roles = ['staff']
    template_name = 'snippets/edit_profile.html'
    model = CustomUser
    fields = ['first_name','last_name']
    success_url = reverse_lazy('api_restaurant:esit_profile')
    def get(self,request,pk):
        staff = get_object_or_404(CustomUser,pk = pk)
        if staff != request.user:
            return HttpResponseForbidden("You are not allowed to edit this profile.")
        user_form = UserUpdateForm(instance=staff)
        employee_form = EmployeeUpdateForm(instance=staff.branchstaff)
        context = {
            'user_form': user_form,
            'employee_form': employee_form,
            'staff': staff,
        }
        return render(request, self.template_name, context)
    def post(self,request,pk):
        print(request.POST)
        staff = get_object_or_404(CustomUser,pk = pk)
        if staff != request.user:
            return HttpResponseForbidden("You are not allowed to edit this profile.")
        user_form = UserUpdateForm(request.POST,instance=staff)
        employee_form = EmployeeUpdateForm(request.POST,instance=staff.branchstaff)
        if user_form.is_valid() and employee_form.is_valid():
            user_form.save()
            employee_form.save()
            return render(request, 'snippets/employee_profile.html', {'staff': staff})
        if user_form.invalid():
            messages.error(request, "Please correct the errors in the form.")
            return render(request, self.template_name, { 'user_form': user_form,
                                                    'employee_form': employee_form,
                                                    'staff': staff,
                                                    })
        if employee_form.invalid():
            messages.error(request, "Please correct the errors in the form.")
            return render(request, self.template_name, { 'user_form': user_form,
                                                    'employee_form': employee_form,
                                                    'staff': staff,
                                                    })

        return render(request, self.template_name, { 'user_form': user_form,
                                                    'employee_form': employee_form,
                                                    'staff': staff,
                                                    })