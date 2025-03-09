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


class IndexPage(TemplateView):
    template_name = "restaurant/index.html"

    