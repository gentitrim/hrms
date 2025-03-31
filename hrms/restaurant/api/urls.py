from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('api/get_products/<int:pk>/',views.ProductsView.as_view(),name='get_products'),
    path('api/my_orders/',views.UserOrderListView.as_view(),name='my_orders'),
    path('api/my_orders/<int:pk>/',views.UserOrderDetailView.as_view(),name='my_order_detail'),
    path('api/search_order_by_date/',views.SearchByDate.as_view(),name='search_order_by_date'),
]