from django.shortcuts import render,get_object_or_404 # type: ignore
from django.views import View # type: ignore
from django.views.generic import ListView # type: ignore
from restaurant.models import Products,Order_item,Order
from django.contrib.auth.mixins import LoginRequiredMixin # type: ignore
from django.db.models import Sum # type: ignore
from django.http import HttpResponseForbidden # type: ignore
import logging
import datetime


logger = logging.getLogger(__name__)

class ProductsView(ListView):
    def get_queryset(self):
        return Products.objects.filter(category_id=self.kwargs['pk'])
    template_name = "snippets/product_list_by_category.html"
    context_object_name = "all_products"


class UserOrderListView(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'snippets/my_order_list.html'
    context_object_name = 'orders'
    login_url = 'login'
    redirect_field_name = 'next'
    paginate_by = 10
    def get_queryset(self):
        self.date = self.request.GET.get('search_date') or datetime.date.today()
        return Order.objects.filter(staff_id=self.request.user.id, order_time__date=self.date).order_by('-order_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        selected_date = datetime.date.today()
        total_amount = self.get_queryset().filter(status='CONFIRMED', order_time__date=selected_date).aggregate(Sum('total_price'))['total_price__sum'] or 0
        context['total_amount'] = total_amount / 100

        return context
    

class UserOrderDetailView(LoginRequiredMixin,View):
    def get(self,request,pk):
        order = get_object_or_404(Order,pk=pk)
        if order.staff_id != request.user:
            return HttpResponseForbidden("You are not allowed to view this order.")
        order_items = Order_item.objects.filter(order_id=order.pk)
        context = {
            'order': order,
            'order_items': order_items,
        }
        return render(request, 'snippets/my_order_detail.html', context)
    

class SearchByDate(LoginRequiredMixin,View):
    def get(self,request):
        date = request.GET.get('search_date') or datetime.date.today()
        print(f"Raw request body: {date}")
        logger.debug(f"Raw request body: {date}")
        orders = Order.objects.filter(order_time__date=date,staff_id=request.user).order_by('-order_time')
        order_items = Order_item.objects.filter(order_id__in=orders)
        
        # Calculate total_amount for the selected date
        total_amount = orders.filter(status='CONFIRMED').aggregate(Sum('total_price'))['total_price__sum'] or 0
        
        context = {
            'orders': orders,
            'order_items': order_items,
            'total_amount': total_amount / 100,
        }
        return render(request, 'snippets/my_order_list.html', context)
