from django.shortcuts import render,redirect
from user_authentication.models import CustomUser
from user_authentication.forms import CustomUserRegisterForm,CustomLoginForm,CustomLogoutForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView,View,UpdateView,ListView,DeleteView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
@login_required
def redirect_by_role(request):
    user = request.user
    role = user.branchstaff.role

    if role == 'admin':
        return redirect('main_management:management_dashboard') 

    elif role == 'manager':
        return redirect('branch_management:manager-dashboard')
    elif role == 'staff':
        return redirect('restaurant:order_menu')
    else:
        return redirect('/')

class UserRegistrationView(LoginRequiredMixin,CreateView):
    form_class = CustomUserRegisterForm
    model = CustomUser
    template_name = 'user_registration.html'
    success_url = reverse_lazy('user_authentication:login')

class UserListView(LoginRequiredMixin,ListView):
    model = CustomUser
    template_name = ("users_list.html") 
    context_object_name = ('users')

class UserUpdateView(LoginRequiredMixin,UpdateView):
    form_class = CustomUserRegisterForm
    model = CustomUser
    template_name = 'user_registration.html'
    success_url = reverse_lazy('user_authentication:users')


class UserDeleteView(LoginRequiredMixin,DeleteView):
    template_name = 'user_delete.html'
    model = CustomUser
    success_url = reverse_lazy('user_authentication:users')
    

class CustomUserLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'user_login.html'

    
    success_url = reverse_lazy('restaurant')



class ConfirmLogoutView(LoginRequiredMixin,LogoutView):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect('user_authentication:login')

