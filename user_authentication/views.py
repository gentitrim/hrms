from django.shortcuts import render,redirect
from user_authentication.models import CustomUser
from user_authentication.forms import CustomUserRegisterForm,CustomLoginForm,CustomLogoutForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView,View,UpdateView,ListView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import logout

# Create your views here.

class UserRegistrationView(CreateView):
    form_class = CustomUserRegisterForm
    model = CustomUser
    template_name = 'user_registration.html'
    success_url = reverse_lazy('restaurant/order_menu')

class UserListView(ListView):
    model = CustomUser
    template_name = ("users_list.html") 
    context_object_name = ('users')

class UserUpdateView(UpdateView):
    form_class = CustomUserRegisterForm
    model = CustomUser
    template_name = 'user_registration.html'
    success_url = reverse_lazy('users')


class UserDeleteView(DeleteView):
    template_name = 'user_delete.html'
    model = CustomUser
    success_url = reverse_lazy('users')
    






class CustomUserLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'user_login.html'
    success_url = reverse_lazy('restaurant')

class LogoutView(View):
    def get(self,request):
        form = CustomLogoutForm
        return render(request, 'user_login.html', {'form': form})

    def post(self, request):
        logout(request)  # Mbyll sesionin e përdoruesit
        return redirect('user-login')


