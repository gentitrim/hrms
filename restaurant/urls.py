from django.urls import path
from . import views
from user_authentication.views import LogoutView,CustomUserLoginView


urlpatterns = [
    # path('',views.IndexPage.as_view(),name="restaurant"),
    path('dashboard/',views.employ_dashboard,name='dashboard'),
    path('order_menu/',views.OrderMenuView.as_view(),name="order_menu"),
    path('shifts/',views.shifts,name="shifts"),
    path('login/',views.login,name='login'),
    path('create_menu/',views.CreateCategoryView.as_view(),name='create_menu'),
    path('confirm_order/',views.confirm_order,name='confirm_order'),
    path('my_orders/',views.UserOrderListView.as_view(),name='my_orders'),
]