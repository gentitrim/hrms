from django.shortcuts import render,redirect,get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Branch,BranchManager
from branch_management.models import BranchStaff
from user_authentication.models import CustomUser
from user_authentication.forms import CustomUserRegisterForm
from .forms import BranchForm,ManagerForm
from django.views.generic import TemplateView,ListView ,FormView, DeleteView,CreateView,UpdateView,DetailView,View
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.


class MainPage(TemplateView):
    def get(self, request):
        return render(request,'management/main.html')
    
class BranchListView(ListView):
    paginate_by = 3
    model = Branch
    template_name = 'management/branches_list.html'
    ordering = ['name']
    # context_object_name = 'branches'

class CreateBranchView(FormView):
    template_name = 'management/create_branch.html'
    success_url = reverse_lazy('management_dashboard')
    form_class = BranchForm
    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        try:
            Branch.objects.create(
                name = cleaned_data["name"],
                address = cleaned_data["address"],
                phone = cleaned_data["phone"],
                email = cleaned_data["email"],
            )
            return super().form_valid(form)
        except Exception as e:
            return HttpResponse(f"Error: {e}", status=500)
    def form_invalid(self, form):
        return super().form_invalid(form)
    

class SearchBranchView(ListView):
    template_name = 'management/branches_list.html'
    paginate_by = 3
    model = Branch
    context_object_name = 'branches'

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        if search:
            return Branch.objects.filter(Q(name__icontains=search)).order_by('name')
        return Branch.objects.all().order_by('name')
    
class EditBranchView(FormView):
    template_name = 'management/edit_branch.html'
    success_url = 'management/branches'
    form_class = BranchForm
    
    def form_valid(self, form):
        return super().form_valid(form)
    
class DeleteBranchView(DeleteView):
    template_name = 'management/delete_branch.html'
    success_url = 'management/branches'


class ManagerManagementView(TemplateView):
    def get(self,request):
        return render(request,'management/manage_manager.html')



class ManagerListView(ListView):
    model = BranchStaff
    template_name = 'management/manage_manager.html'
    context_object_name = 'managers'
    paginate_by = 5

    def get_queryset(self):
        return BranchStaff.objects.filter(role='manager')

    def render_to_response(self, context, **response_kwargs):
        # Kthen partial HTML për HTMX (pa base template)
        if self.request.htmx:
            return super().render_to_response(context, **response_kwargs)
        # Opsional: Redirect ose fallback në një faqe tjetër nëse s’është HTMX
        return super().render_to_response(context, **response_kwargs)
    

class CreateManagerView(View):

    template_name = 'management/create_manager.html'
    success_url = reverse_lazy('manager_list')

    def get(self, request):
        manager_form = ManagerForm()
        user_form = CustomUserRegisterForm()
        return render(request, self.template_name, {
            'managerform': manager_form,
            'userform': user_form
        })

    def post(self, request):
        manager_form = ManagerForm(request.POST)
        user_form = CustomUserRegisterForm(request.POST)

        if user_form.is_valid() and manager_form.is_valid():
            user = user_form.save(commit=False)
            user.is_staff = True  # ose ndonjë atribut tjetër për menaxherin
            user.save()

            manager = manager_form.save(commit=False)
            manager.user = user
            manager.role = 'manager'
            manager.branch = Branch.objects.get(branch_manager__user_id=request.user.id)
            manager.save()

            if request.htmx:
                return HttpResponse(status=204, headers={'HX-Redirect': str(self.success_url)})
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'managerform': manager_form,
            'userform': user_form,
            'manager_errors': manager_form.errors,
            'user_errors': user_form.errors
        })
    

class ManagerUpdateView(UpdateView):
    model = BranchStaff
    form_class = ManagerForm
    template_name = 'management/manager_edit.html'
    context_object_name = 'manager'

    def get_success_url(self):
        return reverse_lazy('manager_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.htmx:
            response['HX-Redirect'] = self.get_success_url()
        return response
    

class ManagerDeleteView(DeleteView):
    model = BranchStaff
    template_name = 'management/manager_delete.html'
    context_object_name = 'manager'

    def get_success_url(self):
        return reverse_lazy('manager_list')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if request.htmx:
            response['HX-Redirect'] = self.get_success_url()
        return response

    

class ManagerDetailView(DetailView):
    model = BranchStaff
    template_name = 'management/manager_detail.html'
    context_object_name = 'manager'

    def get_object(self, queryset=None):
        return get_object_or_404(BranchStaff, id=self.kwargs.get('pk'))
       

    
    

