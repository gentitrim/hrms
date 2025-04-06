from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('create_product/', views.CreateProductView.as_view(), name='create_product'),
    #path('product_list/', views.ProductListView.as_view(), name='product_list'),
    #path('update_product/<int:pk>/', views.ProductUpdateView.as_view(), name='update_product'),
    #path('delete_product/<int:pk>/', views.ProductDeleteView.as_view(), name='delete_product'),
    
    #path('create_category/', views.CreateCategoryView.as_view(), name='create_category'),
    #path('category_list/', views.CategoryListView.as_view(), name='category_list'),

    #path('create_branch_staff/', views.CreateBranchStaff.as_view(), name='create_branch_staff'),
]