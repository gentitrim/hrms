from django.urls import path
from . import views


urlpatterns = [
    # path('',views.IndexPage.as_view(),name="restaurant"),
    path('dashboard/',views.employ_dashboard,name='dashboard'),
    path('order_menu/',views.OrderMenuView.as_view(),name="order_menu"),
    path('shifts/',views.shifts,name="shifts"),
    path('login/',views.login,name='login'),
    path('create_menu/',views.CreateCategoryView.as_view(),name='create_menu'),
]