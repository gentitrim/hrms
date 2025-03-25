from django.shortcuts import render,get_object_or_404
from django.views import View
from django.views.generic import TemplateView,FormView,ListView,View
from .models import Products,Categories,Order,Order_item,BranchStaff
from user_authentication.models import CustomUser
from .forms import CategoryCreateForm,CancelOrderForm
from django.urls import reverse_lazy
from django.http import JsonResponse,HttpResponse
import json
import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# def restaurant(request):
#     return render(request,'restaurant/index.html')

logger = logging.getLogger(__name__)



class OrderMenuView(LoginRequiredMixin,ListView):
    template_name = 'restaurant/employees_dashboard/orders.html'
    model = Categories
    context_object_name = "categories"
    login_url = reverse_lazy('login')
    redirect_field_name = "next"
    

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
            return HttpResponse('Order cancelled successfully', status=200)
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
        logger.debug(f"Received items: {items}")

        total_price = sum(item['total_price'] for item in items) * 100

        #per test deri sa te lidhet user 
        # staff = BranchStaff.objects.get(pk=request.user.id)
        print(request.user.id)
        order = Order.objects.create(total_price=total_price,staff_id = request.user )

        for item in items:
            product = Products.objects.get(pk=item['product_id'])
            Order_item.objects.create(order_id = order,product_id=product,quantity = item['quantity'],price = item['price']*item["quantity"]*100) 

        return JsonResponse({'status': 'success', 'message': 'Order confirmed', 'data': items})

    except json.JSONDecodeError as e:
        logger.error(f"JSONDecodeError: {e}")
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)



class CreateCategoryView(LoginRequiredMixin,FormView):
    template_name = "restaurant/create_menu.html"
    form_class = CategoryCreateForm
    success_url = reverse_lazy('create_menu')
    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        Categories.objects.create(
            name=cleaned_data["name"],
        )
        return super().form_valid(form)

class CreateProductsView(LoginRequiredMixin,FormView):
    template_name = "restaurant/create_menu.html"
    form_class = CategoryCreateForm
    success_url = reverse_lazy('create_menu')
    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        Categories.objects.create(
            name=cleaned_data["name"],
        )
        return super().form_valid(form)