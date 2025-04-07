from django.shortcuts import render
from .models import Branch
from .forms import BranchForm,ManagerForm
from django.views.generic import TemplateView,ListView ,FormView, DeleteView
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

class ManagerListView(ListView):
    template_name = 'management/create_manager.html'
    form_class = ManagerForm
    context_object_name = 'managers'

class CreateManagerView(FormView):
    template_name = 'management/create_manager.html'
    form_class = ManagerForm
    success_url = reverse_lazy('management_dashboard')
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

class UpdateManagerView(FormView):
    template_name = 'management/update_manager.html'
    form_class = ManagerForm
    success_url = '/'

class DeleteManagerView(DeleteView):
    template_name = 'management/delete_manager.html'
    success_url = '/'

