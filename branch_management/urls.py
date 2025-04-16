from django.urls import path
from . import views

app_name = 'branch_management'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='manager-dashboard'),
    path('product/create/', views.CreateProductView.as_view(), name='create-product'),
    path('product/list/', views.ProductListView.as_view(), name='product-list'),
    path('product/list/edit//<int:pk>', views.ProductUpdateView.as_view(), name='update-product'),
    path('product/list/delete/<int:pk>', views.ProductDeleteView.as_view(), name='delete-product'),

    path('employees/', views.EmployeeListView.as_view(), name='employee-list'),
    path('employees/create/', views.EmployeeCreateView.as_view(), name='create_employee'),
    path('employees/update/<int:id>/', views.UpdateEmployeeView.as_view(), name='update_employee'),
    path('employees/delete/<int:pk>/', views.DeleteEmployeeView.as_view(), name='delete_employee'),
    path('employees/detail/<int:pk>/', views.DetailEmployeeView.as_view(), name='detail_employee'),
    # path('', views.ManagerDashboardView.as_view(), name='manager_dashboard'),


    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/update/<int:pk>', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/delete/<int:pk>', views.CategoryDeleteView.as_view(), name='category-delete'),
]