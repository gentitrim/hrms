from django.shortcuts import render,get_object_or_404
from django.views import View
from django.views.generic import TemplateView,FormView,ListView
from restaurant.models import Products,Categories
from restaurant.forms import CategoryCreateForm
from django.urls import reverse_lazy
from django.http import JsonResponse


class ProductsView(ListView):
    def get_queryset(self):
        return Products.objects.filter(category_id=self.kwargs['pk'])
    template_name = "snippets/order_product_list.html"
    context_object_name = "all_products"

class OrderItemVIew(ListView):
    def get_queryset(self):
        return Products.objects.filter(id =self.kwargs['pk'])
    template_name = "snippets/order_items.html"