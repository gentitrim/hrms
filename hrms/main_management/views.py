from django.shortcuts import render
from .models import Branch
from .forms import BranchForm,ManagerForm
from django.views.generic import TemplateView,ListView ,FormView, DeleteView
# Create your views here.


class MainPage(TemplateView):
    def get(self, request):
        return render(request,'management/main.html')
    
class BranchListView(ListView):
    model = Branch
    template_name = 'management/branches_list.html'
    context_object_name = 'branches'

class CreateBranchView(FormView):
    template_name = 'management/create_manager.html'
    success_url = 'management/branches'
    form_class = BranchForm
    
    def form_valid(self, form):
        return super().form_valid(form)
    
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
    success_url = '/'

class UpdateManagerView(FormView):
    template_name = 'management/update_manager.html'
    form_class = ManagerForm
    success_url = '/'

class DeleteManagerView(DeleteView):
    template_name = 'management/delete_manager.html'
    success_url = '/'

