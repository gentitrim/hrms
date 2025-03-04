from django.shortcuts import render,get_object_or_404
from django.views import View
from django.views.generic import TemplateView,FormView,ListView
from .models import Products,Categories
from .forms import CategoryCreateForm
from django.urls import reverse_lazy
from django.http import JsonResponse

# Create your views here.
# def restaurant(request):
#     return render(request,'restaurant/index.html')

def order_menu(request):     
    categories = Categories.objects.all() 
    return render(request,'restaurant/order_menu.html',context={"categories":categories})

class ProductsView(ListView):
    def get_queryset(self):
        return Products.objects.filter(category_id=self.kwargs['pk'])
    template_name = "snippets/order_product_list.html"


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
def info(request):
    return render(request,'restaurant/info.html')

def shifts(request):
    return render(request,'restaurant/shifts.html')

def login(request):
    return render(request,'restaurant/login.html')


class IndexPage(TemplateView):
    template_name = "restaurant/index.html"

    