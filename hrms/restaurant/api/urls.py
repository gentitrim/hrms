from django.urls import path
from . import views

urlpatterns = [
    path('api/get_products/<int:pk>/',views.ProductsView.as_view(),name='get_products'),
    path('api/my_orders/',views.UserOrderListView.as_view(),name='my_orders'),
]