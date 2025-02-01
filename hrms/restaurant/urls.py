from django.urls import path
from . import views


urlpatterns = [
    path('',views.restaurant),
    path('info/',views.info,name='info'),
    path('order_menu/',views.order_menu,name="order_menu"),
    path('shifts/',views.shifts,name="shifts"),
    path('login/',views.login,name='login'),
]