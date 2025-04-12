from django.urls import path
from main_management import views
# from user_authentication.views import LogoutView,CustomUserLoginView


urlpatterns = [
    path('',views.MainPage.as_view(),name='management_dashboard'),
    path('manage_branch/',views.BranchListView.as_view(),name = 'branch'),
    path('create_new_branch/',views.CreateBranchView.as_view(),name = 'new_branch'),
    path('update_branch/',views.CreateBranchView.as_view(),name = 'update_branch'),
    path('delete_branch/',views.DeleteBranchView.as_view(),name = 'delete_branch'),
    path('search_branch/',views.SearchBranchView.as_view(),name = 'search_branch'),
    path('manage_managers/', views.ManagerManagementView.as_view(), name='manage_managers'),
    path('managers/', views.ManagerListView.as_view(), name='manager_list'),
    path('managers/create/', views.CreateManagerView.as_view(), name='create_manager'),
    path('managers/<int:pk>/edit/', views.ManagerUpdateView.as_view(), name='edit_manager'),    
    path('managers/<int:pk>/delete/', views.ManagerDeleteView.as_view(), name='delete_manager'),
    path('managers/<int:pk>/', views.ManagerDetailView.as_view(), name='manager_detail'),
    
]