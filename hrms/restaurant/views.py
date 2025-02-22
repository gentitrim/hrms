from django.shortcuts import render

# Create your views here.
def restaurant(request):
    return render(request,'restaurant/index.html')


def order_menu(request):
    return render(request,'restaurant/order_menu.html')

def info(request):
    return render(request,'restaurant/info.html')

def shifts(request):
    return render(request,'restaurant/shifts.html')

def login(request):
    return render(request,'restaurant/login.html')

def create_menu(request):
    return render(request,'restaurant/create_menu.html')

