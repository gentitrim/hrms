from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
import json
import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import datetime
from hrms.rolemixin import RoleAccessMixin
from .models import Order, Order_item
from branch_management.models import BranchStaff, Product, Category
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from user_authentication.models import CustomUser
from user_authentication.forms import CustomUserResetPassForm
from django.views import View
from django.shortcuts import redirect


class CategoryListView(LoginRequiredMixin,RoleAccessMixin,ListView):
    allowed_roles = ['staff']
    template_name = 'restaurant/employees_dashboard/orders.html'
    model = Category
    context_object_name = "categories"
    login_url = reverse_lazy('user_authentication:login')
    redirect_field_name = "next"

    def get_queryset(self):
        user_branch = self.request.user.branchstaff.branch
        return Category.objects.filter(branch=user_branch)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_branch = self.request.user.branchstaff.branch
        
        orders = Order.objects.filter(staff_id__branch=user_branch)

        
        date_str = self.request.GET.get('date', None)
        try:
            if date_str:
                selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                orders = orders.filter(order_time__date=selected_date)
            else:
                
                orders = orders.filter(order_time__date=timezone.now().date())
        except ValueError:
            
            orders = orders.filter(order_time__date=timezone.now().date())

        context['orders'] = orders
        context['selected_date'] = date_str or timezone.now().date().strftime('%Y-%m-%d')
        return context

class DashboardView(LoginRequiredMixin,RoleAccessMixin,TemplateView):
    allowed_roles = ['staff']
    template_name = 'restaurant/employees_dashboard/dashboard.html'
    login_url = reverse_lazy('user_authentication:login')
    redirect_field_name = "next"


class CancelOrderView(LoginRequiredMixin,RoleAccessMixin, TemplateView):
    allowed_roles = ['staff']
    template_name = 'restaurant/employees_dashboard/cancel_order.html'
    login_url = reverse_lazy('user_authentication:login')
    redirect_field_name = "next"

    def post(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(pk=self.kwargs['pk'])
            order.status = 'CANCELED'
            order.save()
            
            user_branch = self.request.user.branchstaff.branch
            orders = Order.objects.filter(staff_id__branch=user_branch)
            date_str = self.request.GET.get('date', None)
            try:
                if date_str:
                    selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    orders = orders.filter(order_time__date=selected_date)
                else:
                    orders = orders.filter(order_time__date=timezone.now().date())
            except ValueError:
                orders = orders.filter(order_time__date=timezone.now().date())
            return render(request, 'snippets/my_order_list.html', {'orders': orders})
        except Order.DoesNotExist:
            return HttpResponse('Order not found', status=404)
        except Exception as e:
            return HttpResponse(str(e), status=500)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(pk=self.kwargs['pk'])
        return context


class ShiftsView(LoginRequiredMixin,RoleAccessMixin,TemplateView):
    allowed_roles = ['staff']
    template_name = 'restaurant/employees_dashboard/shifts.html'
    login_url = reverse_lazy('user_authentication:login')
    redirect_field_name = "next"


@login_required
def confirm_order(request):
    if request.user.branchstaff.role != 'staff':
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
    try:
        raw_body = request.body.decode('utf-8')

        data = json.loads(raw_body)

        if 'items' not in data or not data['items']:
            return JsonResponse({'status': 'error', 'message': 'No items provided'}, status=400)

        items = data['items']

        total_price = sum(item['total_price'] for item in items) * 100

        staff = get_object_or_404(BranchStaff, pk=request.user.branchstaff.id)
        order = Order.objects.create(total_price=total_price, staff_id=staff)

        for item in items:
            product = Product.objects.get(pk=item['product_id'])
            Order_item.objects.create(
                order_id=order,
                product_id=product,
                quantity=item['quantity'],
                price=item['price'] * item["quantity"] * 100
            )
        
        # 🔥 Kjo është pjesa e re që duhet shtuar:
        order.confirm_order()

        return JsonResponse({'status': 'success', 'message': 'Order confirmed', 'data': items})

    except json.JSONDecodeError as e:
        messages.error(request, f"JSONDecodeError: {e}")
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

    except Exception as e:
        messages.error(request, f"Unexpected error: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    


class ResetPasswordView(LoginRequiredMixin, RoleAccessMixin, View):
    allowed_roles = ["staff"]
    template_name = "snippets/reset_password_employee.html"
    success_url = reverse_lazy("api_restaurant:my_profile")
    login_url = reverse_lazy("user_authentication:login")
    redirect_field_name = "next"

    def get(self, request, pk):
        staff_user = get_object_or_404(CustomUser, pk=pk)
        form = CustomUserResetPassForm()
        return render(
            request, self.template_name, {"form": form, "staff_user": staff_user}
        )

    def post(self, request, pk):
        staff_user = get_object_or_404(CustomUser, pk=pk)
        form = CustomUserResetPassForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data["new_password"]
            staff_user.set_password(new_password)
            staff_user.save()
            messages.success(
                request, f"Password for {staff_user.username} has been changed."
            )
            return redirect("user_authentication:login")  # or any page you want
        messages.error(request, "Please complete in the correct form.")
        return render(
            request, self.success_url, {"form": form, "staff_user": staff_user}
        )

