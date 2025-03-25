from django.shortcuts import render,get_object_or_404
from django.views import View
from django.views.generic import TemplateView,FormView,ListView
from restaurant.models import Products,Categories
from restaurant.forms import CategoryCreateForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from restaurant.order import Order



class ProductsView(ListView):
    def get_queryset(self):
        return Products.objects.filter(category_id=self.kwargs['pk'])
    template_name = "snippets/order_product_list.html"
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

def add_product_to_session(request):
    pass