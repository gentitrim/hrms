from django.urls import path
from . import views

urlpatterns = [
    path('api/get_products/<int:pk>/',views.ProductsView.as_view(),name='get_products'),
    path('order_detail/',views.order_detail,name='order_detail'),
    path('add_order/',views.order_detail,name='add_order'),
    path('delete_detail/',views.order_detail,name='delete_detail'),
    path('update_order/',views.order_detail,name='update_order'),
    # path('api/add-to-order/<int:pk>/', views.session_item_in_order, name='add_to_cart'),
]
