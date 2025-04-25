from django.urls import path
from user_authentication.views import (UserRegistrationView,
                                       CustomUserLoginView,
                                       ConfirmLogoutView,
                                       UserUpdateView,
                                       UserListView,
                                       UserDeleteView,
                                       redirect_by_role)


app_name ='user_authentication'

urlpatterns = [
    path('user/register/',UserRegistrationView.as_view(), name='user-register' ),
    path('users/' ,UserListView.as_view(), name='users' ),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name = 'update-user'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name = 'delete-user'),
    path('', CustomUserLoginView.as_view(), name = 'login'),
    path('logout/', ConfirmLogoutView.as_view(), name='logout'),
    path('redirect-by-role/', redirect_by_role, name='redirect_by_role'),
    
    
]