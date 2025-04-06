from django.urls import path
from . import views

app_name = 'branch_management'

urlpatterns = [
    path('employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employees/create/', views.EmployeeCreateView.as_view(), name='create_employee'),
    path('employees/update/<int:id>/', views.update_employee, name='update_employee'),
    path('employees/delete/<int:id>/', views.delete_employee, name='delete_employee'),
    path('', views.manager_dashboard, name='manager_dashboard'),  
]