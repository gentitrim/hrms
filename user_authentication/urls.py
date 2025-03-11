from django.urls import path
from user_authentication.views import (UserRegistrationView,
                                       CustomUserLoginView,
                                       LogoutView,
                                       UserUpdateView,
                                       UserListView,
                                       UserDeleteView)
from restaurant.views import IndexPage


urlpatterns = [
    path('restaurant/',IndexPage.as_view(),name="restaurant"),
    path('user/register/',UserRegistrationView.as_view(), name='user-register' ),
    path('users/' ,UserListView.as_view(), name='users' ),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name = 'update-user'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name = 'delete-user'),
    path('user_login/', CustomUserLoginView.as_view(), name = 'user-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    
]