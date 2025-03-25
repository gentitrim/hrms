from django.urls import path
from . import views

urlpatterns = [
    path('api/get_products/<int:pk>/',views.ProductsView.as_view(),name='get_products'),
    # path('api/get_order_item/<int:pk>/',views.OrderItemView.as_view(),name='get_order_items'),
    # path('api/add_product_to_session/<pk>', views.add_order, name='add_to_order'),
]
