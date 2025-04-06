from django.urls import path
from . import views

urlpatterns = [
    path('manager/dashboard/', views.DashboardView.as_view(), name='manager-dashboard'),
    path('create/product/', views.CreateProductView.as_view(), name='create-product'),
    path('product/list/', views.ProductListView.as_view(), name='product-list'),
    path('products/list/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='update-product'),
    path('products/list/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete-product'),
    

    #path('create_category/', views.CreateCategoryView.as_view(), name='create_category'),
    #path('category_list/', views.CategoryListView.as_view(), name='category_list'),

    #path('create_branch_staff/', views.CreateBranchStaff.as_view(), name='create_branch_staff'),
]