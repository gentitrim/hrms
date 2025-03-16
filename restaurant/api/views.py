from django.shortcuts import render,get_object_or_404
from django.views import View
from django.views.generic import TemplateView,FormView,ListView
from restaurant.models import Products,Categories,Order_item,Order
from restaurant.forms import CategoryCreateForm
from django.urls import reverse_lazy
from django.http import JsonResponse
import json


class ProductsView(ListView):
    def get_queryset(self):
        return Products.objects.filter(category_id=self.kwargs['pk'])
    template_name = "snippets/product_list_by_category.html"
    context_object_name = "all_products"

