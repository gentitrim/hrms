from django.shortcuts import render

# Create your views here.
def restaurant(request):
    return render(request,'restaurant/base.html')