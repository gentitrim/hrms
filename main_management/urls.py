from django.urls import path
from . import views
# from user_authentication.views import LogoutView,CustomUserLoginView


urlpatterns = [
    path('',views.MainPage.as_view(),name='management_dashboard'),
    path('manage_branch/',views.BranchListView.as_view(),name = 'branch'),
    path('create_new_branch/',views.CreateBranchView.as_view(),name = 'new_branch'),
    path('update_branch/',views.CreateBranchView.as_view(),name = 'update_branch'),
    path('delete_branch/',views.DeleteBranchView.as_view(),name = 'delete_branch'),
    path('search_branch/',views.SearchBranchView.as_view(),name = 'search_branch'),
    path('create_new_manager/',views.CreateManagerView.as_view(),name = 'new_manager'),
    path('update_manager/',views.UpdateManagerView.as_view(),name = 'update_manager'),
    path('delete_manager/',views.DeleteManagerView.as_view(),name = 'delete_manager'),
]