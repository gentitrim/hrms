from django.urls import path
from . import views

app_name = 'branch_management'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='manager-dashboard'),
    path('product/create/', views.CreateProductView.as_view(), name='create-product'),
    path('product/list/', views.ProductListView.as_view(), name='product-list'),
    path('product/list/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='update-product'),
    path('product/list/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete-product'),

    path('category/create/', views.CreateProductView.as_view(), name='create-category'),
    path('category/list/', views.ProductListView.as_view(), name='category-list'),
    path('category/product-<int:pk>/edit/', views.ProductUpdateView.as_view(), name='update-category'),
    path('category/product-<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete-category'),
    
    path('employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employees/create/', views.EmployeeCreateView.as_view(), name='create_employee'),
    path('employees/update/<int:id>/', views.UpdateEmployeeView.as_view(), name='update_employee'),
    path('employees/delete/<int:pk>/', views.DeleteEmployeeView.as_view(), name='delete_employee'),
    path('', views.ManagerDashboardView.as_view(), name='manager_dashboard'),  
]