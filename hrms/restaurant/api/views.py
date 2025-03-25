from django.shortcuts import render,get_object_or_404
from django.views import View
from django.views.generic import TemplateView,FormView,ListView
from restaurant.models import Products,Categories,Order_item,Order
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum

class ProductsView(ListView):
    def get_queryset(self):
        return Products.objects.filter(category_id=self.kwargs['pk'])
    template_name = "snippets/product_list_by_category.html"
    context_object_name = "all_products"

def order_total(request):
    return render(request, "products_in_order.html", {})

def add_order(request):
    order = Order(request)
    if request.POST.get('action') == "post":
        product_id = int(request.POST.get(product_id))
        product = get_object_or_404(Products, pk = product_id)
        order.add(product = product)
        response = JsonResponse({"Product name": product.name})
        return response

class UserOrderListView(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'snippets/my_order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(staff_id=self.request.user.id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_amount = self.get_queryset().aggregate(Sum('total_price'))['total_price__sum'] or 0
        context['total_amount'] = total_amount

        return context
    

class UserOrderDetailView(LoginRequiredMixin,View):
    def get(self,request,pk):
        order = get_object_or_404(Order,pk=pk)
        return render(request,'employees_dashboard/order_detail.html',{'order':order})

class UserOrderListView(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'snippets/my_order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(staff_id=self.request.user.id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_amount = self.get_queryset().aggregate(Sum('total_price'))['total_price__sum'] or 0
        context['total_amount'] = total_amount

        return context
    

class UserOrderDetailView(LoginRequiredMixin,View):
    def get(self,request,pk):
        order = get_object_or_404(Order,pk=pk)
        return render(request,'employees_dashboard/order_detail.html',{'order':order})

