from django.urls import path
from . import views

urlpatterns = [
    path('api/get_products/<int:pk>/',views.ProductsView.as_view(),name='get_products'),
    # path('api/get_order_item/<int:pk>/',views.OrderItemView.as_view(),name='get_order_items'),
    path('add-to-order/<pk>/', views.session_item_in_order, name='add_to_cart'),
]
