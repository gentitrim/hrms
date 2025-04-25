from django.urls import path
from main_management import views
# from user_authentication.views import LogoutView,CustomUserLoginView

app_name = 'main_management'

urlpatterns = [
    path('',views.OwnerDashboardView.as_view(),name='owner_dashboard'),
    # path('orders_per_branch/',views.OrdersPerBranchView.as_view(),name='orders_per_branch'),
    # path('orders_per_branch/<int:pk>/',views.OrdersPerBranchView.as_view(),name='orders_per_branch'),


    path('',views.MainPage.as_view(),name='management_dashboard'),
    path('manage_branch/',views.BranchListView.as_view(),name = 'branch'),
    path('create_new_branch/',views.CreateBranchView.as_view(),name = 'new_branch'),
    path('update_branch/<int:pk>',views.EditBranchView.as_view(),name = 'update_branch'),
    path('delete_branch/<int:pk>',views.DeleteBranchView.as_view(),name = 'delete_branch'),
    path('search_branch/',views.SearchBranchView.as_view(),name = 'search_branch'),
    path('branch/<int:pk>/',views.BranchDetailView.as_view(),name = 'branch_detail'),
    
    
    path('managers/', views.ManagerListView.as_view(), name='manager_list'),
    path('managers/create/', views.CreateManagerView.as_view(), name='create_manager'),
    path('managers/<int:pk>/edit/', views.ManagerUpdateView.as_view(), name='edit_manager'),    
    path('managers/<int:pk>/delete/', views.ManagerDeleteView.as_view(), name='delete_manager'),
    path('managers/<int:pk>/', views.ManagerDetailView.as_view(), name='manager_detail'),
    path('manager/reset_password/<int:pk>/', views.ManagerResetPasswordView.as_view(), name='manager_reset_password'),
    # path('manager/<int:pk>/change_password/', views.ManagerChangePasswordView.as_view(), name='manager_change_password'),
    path('profile/', views.ProfileView.as_view(), name='your_profile'),
    path('profile/edit/<int:pk>/', views.EditProfileView.as_view(), name='edit_profile'),
    
    path('all-employees/', views.AllEmployeesListView.as_view(), name='all_employees'),
]