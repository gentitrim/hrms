from django.views.generic import TemplateView,ListView # type: ignore
from .models import Order,Order_item # type: ignore
from branch_management.models import BranchStaff,Product,Category
from django.shortcuts import get_object_or_404 # type: ignore
from django.urls import reverse_lazy # type: ignore
from django.http import JsonResponse,HttpResponse # type: ignore
import json
import logging
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin# type: ignore


logger = logging.getLogger(__name__)



class CategoryListView(LoginRequiredMixin,ListView):
    template_name = 'restaurant/employees_dashboard/orders.html'
    model = Category
    context_object_name = "categories"
    login_url = reverse_lazy('login')
    redirect_field_name = "next"
    
    def get_queryset(self):
            user_branch = self.request.user.branchstaff.branch
            return Category.objects.filter(branch=user_branch)

class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'restaurant/employees_dashboard/dashboard.html'
    login_url = reverse_lazy('login')
    redirect_field_name = "next"


class CancelOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'restaurant/employees_dashboard/cancel_order.html'
    login_url = reverse_lazy('login')
    redirect_field_name = "next"

    def post(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(pk=self.kwargs['pk'])
            order.status = 'CANCELED'
            order.save()
            return HttpResponse('Order canceled successfully', status=200)
        except Order.DoesNotExist:
            return HttpResponse('Order not found', status=404)
        except Exception as e:
            return HttpResponse(str(e), status=500)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(pk=self.kwargs['pk'])
        return context


class ShiftsView(LoginRequiredMixin,TemplateView):
    template_name = 'restaurant/employees_dashboard/shifts.html'
    login_url = reverse_lazy('login')
    redirect_field_name = "next"


@login_required
def confirm_order(request):
    try:
        raw_body = request.body.decode('utf-8')
        logger.debug(f"Raw request body: {raw_body}")
        print(request.user.id)

        data = json.loads(raw_body)
        logger.debug(f"Parsed JSON data: {data}")

        if 'items' not in data or not data['items']:
            return JsonResponse({'status': 'error', 'message': 'No items provided'}, status=400)

        items = data['items']
        # logger.debug(f"Received items: {items}")

        total_price = sum(item['total_price'] for item in items) * 100

        #For test until branch staff is created
        staff = get_object_or_404(BranchStaff,pk=request.user.branchstaff.id)
        order = Order.objects.create(total_price=total_price,staff_id=staff )
        print(staff)
        for item in items:
            product = Product.objects.get(pk=item['product_id'])
            Order_item.objects.create(order_id = order,product_id=product,quantity = item['quantity'],price = item['price']*item["quantity"]*100) 

        return JsonResponse({'status': 'success', 'message': 'Order confirmed', 'data': items})

    except json.JSONDecodeError as e:
        logger.error(f"JSONDecodeError: {e}")
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
