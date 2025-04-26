from django.urls import path
from . import views
# from user_authentication.views import LogoutView,CustomUserLoginView


app_name = 'restaurant'

urlpatterns = [
    # path('',views.IndexPage.as_view(),name="restaurant"),
    path('dashboard/',views.DashboardView.as_view(),name='dashboard'),
    path('order_menu/',views.CategoryListView.as_view(),name="order_menu"),
    path('shifts/',views.ShiftsView.as_view(),name="shifts"),
    path('confirm_order/',views.confirm_order,name='confirm_order'),
    path('cancel_order/<int:pk>/',views.CancelOrderView.as_view(),name='cancel_order'),
    path('reset_your_password/<int:pk>/',views.ResetPasswordView.as_view(),name='edit_password'),
     path('increase-quantity/', views.increase_quantity, name='increase_quantity'),
    path('decrease-quantity/', views.decrease_quantity, name='decrease_quantity'),
]