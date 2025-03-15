from django.shortcuts import render,get_object_or_404
from django.views import View
from django.views.generic import TemplateView,FormView,ListView
from .models import Products,Categories,Order,Order_item,BranchStaff
from .forms import CategoryCreateForm,ConfirmOrderForm
from django.urls import reverse_lazy
from django.http import JsonResponse
import json
import logging

# Create your views here.
# def restaurant(request):
#     return render(request,'restaurant/index.html')

logger = logging.getLogger(__name__)

genti = BranchStaff()


class OrderMenuView(ListView):
    template_name = 'restaurant/employees_dashboard/orders.html'
    model = Categories
    context_object_name = "categories"


class CreateCategoryView(FormView):
    template_name = "restaurant/create_menu.html"
    form_class = CategoryCreateForm
    success_url = reverse_lazy('create_menu')
    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        Categories.objects.create(
            name=cleaned_data["name"],
        )
        return super().form_valid(form)

class CreateProductsView(FormView):
    template_name = "restaurant/create_menu.html"
    form_class = CategoryCreateForm
    success_url = reverse_lazy('create_menu')
    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        Categories.objects.create(
            name=cleaned_data["name"],
        )
        return super().form_valid(form)
    

def employ_dashboard(request):
    return render(request,'restaurant/employees_dashboard/dashboard.html')

def shifts(request):
    return render(request,'restaurant/shifts.html')

def login(request):
    return render(request,'restaurant/login.html')


def confirm_order(request):
    try:
        raw_body = request.body.decode('utf-8')
        logger.debug(f"Raw request body: {raw_body}")

        data = json.loads(raw_body)
        logger.debug(f"Parsed JSON data: {data}")

        if 'items' not in data:
            return JsonResponse({'status': 'error', 'message': 'No items provided'}, status=400)

        items = data['items']
        logger.debug(f"Received items: {items}")

        total_price = sum(item['total_price'] for item in items)

        order = Order.objects.create(total_price=total_price,staff_id = BranchStaff.objects.get(pk = 1))

        for item in items:
            Order_item.objects.create(order_id = order,product_id=Products.objects.get(pk=item['product_id']),quantity = item['quantity'],price = item['total_price'] )

        return JsonResponse({'status': 'success', 'message': 'Order confirmed', 'data': items})

    except json.JSONDecodeError as e:
        logger.error(f"JSONDecodeError: {e}")
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)