from django.shortcuts import render,redirect,get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from main_management.models import Branch
from branch_management.models import BranchStaff
from main_management.forms import BranchForm,ManagerForm
from django.views.generic import TemplateView,ListView ,FormView, DeleteView,CreateView,UpdateView,DetailView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db.models import Q