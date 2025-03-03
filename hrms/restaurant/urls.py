from django.urls import path
from . import views


urlpatterns = [
    path('',views.IndexPage.as_view(),name="restaurant"),
    path('info/',views.info,name='info'),
    path('order_menu/',views.order_menu,name="order_menu"),
    path('shifts/',views.shifts,name="shifts"),
    path('login/',views.login,name='login'),
    path('create_menu/',views.CreateCategoryView.as_view(),name='create_menu'),
    path('get_roducts/<pk>/',views.get_products,name='get_prducts')
]