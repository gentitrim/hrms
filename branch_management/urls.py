from django.urls import path
from . import views

app_name = 'branch_management'

urlpatterns = [
    path('employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employees/create/', views.EmployeeCreateView.as_view(), name='create_employee'),
    path('employees/update/<int:id>/', views.UpdateEmployeeView.as_view(), name='update_employee'),
    path('employees/delete/<int:pk>/', views.DeleteEmployeeView.as_view(), name='delete_employee'),
    path('', views.ManagerDashboardView.as_view(), name='manager_dashboard'),  
]