from django.urls import path
from user_authentication.views import UserRegistrationView,CustomUserLoginView,LogoutView
from restaurant.views import IndexPage


urlpatterns = [
    path('restaurant/',IndexPage.as_view(),name="restaurant"),
    path('user/register/',UserRegistrationView.as_view(), name='user-register' ),
    path('user_login/', CustomUserLoginView.as_view(), name = 'user-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    
]